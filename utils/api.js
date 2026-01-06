/**
 * 模拟 API 服务模块 - 极简高可靠版
 * 专注于本地静态数据加载，支持 H5 和微信小程序
 */

// 1. 核心改进：通过 Import 直接通过 JS 引擎加载主数据，彻底解决小程序 FS 路径问题
import localProductsJson from '../static/data/products.json';

export const MEMBER_LEVELS = {
    NORMAL: { name: '普通会员', discount: 1.0, color: '#7F8C8D', bg: 'linear-gradient(135deg, #BDC3C7 0%, #95A5A6 100%)', textColor: '#FFFFFF' },
    SILVER: { name: '白银会员', discount: 0.95, color: '#95A5A6', bg: 'linear-gradient(135deg, #E5E7E9 0%, #BDC3C7 100%)', textColor: '#2C3E50' },
    GOLD: { name: '黄金会员', discount: 0.9, color: '#D4AF37', bg: 'linear-gradient(135deg, #F1C40F 0%, #D4AF37 100%)', textColor: '#FFFFFF' },
    BLACK_GOLD: { name: '黑金会员', discount: 0.8, color: '#D4AF37', bg: 'linear-gradient(135deg, #2C3E50 0%, #000000 100%)', textColor: '#D4AF37', border: '1rpx solid #D4AF37' }
};

export const apiService = {
    _cachedData: null,

    getCurrentMemberLevel() {
        return uni.getStorageSync('memberLevel') || 'BLACK_GOLD';
    },

    calculateMemberPrice(price) {
        const levelKey = this.getCurrentMemberLevel();
        const discount = (MEMBER_LEVELS[levelKey] || MEMBER_LEVELS.BLACK_GOLD).discount;
        return (parseFloat(price || 0) * discount).toFixed(2);
    },

    formatImageUrl(url) {
        if (!url) return '';
        if (url.startsWith('/') || url.startsWith('static/')) return url;
        return url;
    },

    /**
     * 2. 核心改进：针对详情页等动态文件，使用增强的 FS 读取策略
     */
    async _readLocalJson(path) {
        const relativePath = path.startsWith('/') ? path.substring(1) : path;
        
        return new Promise((resolve, reject) => {
            // #ifdef MP-WEIXIN
            try {
                const fs = wx.getFileSystemManager();
                // 尝试路径: 绝对路径(/static/...) 和 包内相对路径(static/...)
                const paths = ['/' + relativePath, relativePath];
                
                for (const p of paths) {
                    try {
                        // 优先尝试 UTF-8 读取，简单直接
                        const content = fs.readFileSync(p, 'utf8');
                        if (content) {
                            // 处理 BOM 头
                            const jsonStr = content.charCodeAt(0) === 0xFEFF ? content.substring(1) : content;
                            return resolve(JSON.parse(jsonStr));
                        }
                    } catch (e) { /* continue */ }
                }
                
                // 如果 UTF-8 失败 (极少见)，尝试异步读取作为兜底
                fs.readFile({
                    filePath: '/' + relativePath,
                    encoding: 'utf8',
                    success: res => resolve(JSON.parse(res.data)),
                    fail: () => {
                        this._requestFallback('/' + relativePath, resolve, reject);
                    }
                });
                return;
            } catch (e) {
                console.warn('[API] FS 错误:', e);
            }
            // #endif

            // H5 环境
            this._requestFallback('/' + relativePath, resolve, reject);
        });
    },

    _requestFallback(url, resolve, reject) {
        uni.request({
            url: url,
            method: 'GET',
            success: (res) => {
                if (res.statusCode === 200) {
                    resolve(res.data);
                } else {
                    reject(new Error('Request failed'));
                }
            },
            fail: reject
        });
    },

    /**
     * 3. 核心改进：主数据加载逻辑极简，直接返回 Import 的数据
     */
    async _loadData() {
        if (this._cachedData) return this._cachedData;
        try {
            console.log('[API] Loading main data via Import...');
            const res = localProductsJson;
            let list = Array.isArray(res) ? res : (res.data?.list || res.list || []);
            this._cachedData = { list, updateTime: res.updateTime || '' };
            return this._cachedData;
        } catch (e) {
            console.error('[API] Data init failed:', e);
            throw e;
        }
    },

    async getProducts(params = { page: 1, pageSize: 12, category: '', keyword: '' }) {
        try {
            const { list } = await this._loadData();
            let filtered = list;

            if (params.category && params.category !== '全部' && params.category !== 'all') {
                const cat = params.category.trim().toLowerCase();
                filtered = filtered.filter(item => 
                    (item.name || '').toLowerCase().includes(cat) || 
                    (item.brand || '').toLowerCase().includes(cat) ||
                    (item.tags || []).some(t => String(t).toLowerCase().includes(cat))
                );
            }

            if (params.keyword) {
                const kw = params.keyword.trim().toLowerCase();
                filtered = filtered.filter(item => 
                    (item.name || '').toLowerCase().includes(kw) || 
                    (item.brand || '').toLowerCase().includes(kw)
                );
            }

            const start = (params.page - 1) * params.pageSize;
            return {
                list: filtered.slice(start, start + params.pageSize),
                total: filtered.length,
                isLocal: true
            };
        } catch (e) {
            return { list: [], total: 0, error: e.message };
        }
    },

    async getProductDetail(id) {
        try {
            // 详情数据量大且文件多，依然使用 FS 动态加载
            const data = await this._readLocalJson(`static/data/details/${id}.json`);
            const raw = Array.isArray(data) ? data[0] : (data.data?.list?.[0] || data.data || data);
            
            if (!raw) throw new Error('Product not found');

            let price = 0;
            try { price = raw.unitList?.[0]?.orderPrice || raw.priceList?.[0]?.unitPrices?.[0]?.orderPrice || 0; } catch(e) {}
            if (price === 0) price = 99;

            return {
                id: raw.id,
                name: raw.name,
                brand: raw.brandName || raw.brand || raw.productBrand?.name || '医美严选',
                price: price,
                originalPrice: Math.round(price * 1.5),
                image: raw.mainImg ? 'https://img.dinghuo123.com/' + raw.mainImg.imgUrl : '',
                album: (raw.albumList || []).map(img => 'https://img.dinghuo123.com/' + img.imgUrl),
                desc: raw.remark || '正品保障，权威认证。',
                detailHtml: (raw.description || raw.introduction || '')
                    .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
                    .replace(/&#60;/g, '<').replace(/&#62;/g, '>')
                    .replace(/&#34;/g, '"').replace(/&quot;/g, '"')
                    .replace(/&#39;/g, "'").replace(/&apos;/g, "'")
                    .replace(/&nbsp;/g, ' ')
                    .replace(/&amp;/g, '&'),
                sales: 100 + (Number(raw.id) % 500)
            };
        } catch (e) {
            console.error('[API] Detail load failed:', id, e);
            throw e;
        }
    },

    async getHomeProducts() {
        const res = await this.getProducts({ page: 1, pageSize: 10 });
        return res.list || [];
    },

    async getCategories() {
        try {
            const { list } = await this._loadData();
            const brands = [...new Set(list.map(p => p.brand).filter(b => b && b !== '未知'))];
            const base = [{ name: '全部', id: 'all' }, { name: '水光', id: 'sg' }, { name: '面膜', id: 'mm' }];
            return [...base, ...brands.slice(0, 15).map(b => ({ name: b, id: b }))];
        } catch (e) {
            return [{ name: '全部', id: 'all' }];
        }
    }
};
