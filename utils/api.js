/**
 * API 服务模块 - 数据库后端版
 * 连接 Flask + SQLite 后端，支持本地化图片服务
 */

// 核心配置：切换为 Flask 后端地址
// 真机调试请将 localhost 改为你的电脑局域网 IP (如 192.168.1.5)
const BASE_URL = 'http://localhost:8080';

export const MEMBER_LEVELS = {
    NORMAL: { name: '普通会员', discount: 1.0, color: '#7F8C8D', bg: 'linear-gradient(135deg, #BDC3C7 0%, #95A5A6 100%)', textColor: '#FFFFFF' },
    SILVER: { name: '白银会员', discount: 0.95, color: '#95A5A6', bg: 'linear-gradient(135deg, #E5E7E9 0%, #BDC3C7 100%)', textColor: '#2C3E50' },
    GOLD: { name: '黄金会员', discount: 0.9, color: '#D4AF37', bg: 'linear-gradient(135deg, #F1C40F 0%, #D4AF37 100%)', textColor: '#FFFFFF' },
    BLACK_GOLD: { name: '黑金会员', discount: 0.8, color: '#D4AF37', bg: 'linear-gradient(135deg, #2C3E50 0%, #000000 100%)', textColor: '#D4AF37', border: '1rpx solid #D4AF37' }
};

export const apiService = {
    getCurrentMemberLevel() {
        return uni.getStorageSync('memberLevel') || 'BLACK_GOLD';
    },
    calculateMemberPrice(price) {
        const levelKey = this.getCurrentMemberLevel();
        const discount = (MEMBER_LEVELS[levelKey] || MEMBER_LEVELS.BLACK_GOLD).discount;
        
        // 利润保护：在打折前加上固定利润，保证最低盈利
        // 这样即使打折，也能保证盈利至少15块
        const PROFIT_MARGIN = 15; // 固定利润15块
        const basePrice = parseFloat(price || 0) + PROFIT_MARGIN;
        
        const memberPrice = (basePrice * discount).toFixed(2);
        console.log(`[API] Price calculation: base=${price} + margin=${PROFIT_MARGIN} = ${basePrice}, discount=${discount}, final=${memberPrice}`);
        
        return memberPrice;
    },
    formatImageUrl(url) {
        if (!url) return '';
        if (url.startsWith('http')) return url;
        
        // 核心修复：清理脏路径，解决路径重复和双斜杠问题
        // 目标是将所有包含 product_images 的路径统一格式化为 static/product_images/xxx
        let path = url.replace(/\\/g, '/'); // Windows路径转正斜杠
        
        if (path.includes('product_images/')) {
            // 无论前面有多少重复的 static 或 product_images，只取最后一个 product_images 及其之后的部分
            const marker = 'product_images/';
            const lastIndex = path.lastIndexOf(marker);
            const cleanSuffix = path.substring(lastIndex); // 得到 product_images/x/y.jpg
            
            // [恢复] 指向后端接口 8080
            return `${BASE_URL}/static/${cleanSuffix}`;
        }

        let cleanUrl = path;
        if (cleanUrl.startsWith('/')) cleanUrl = cleanUrl.substring(1);
        return 'https://img.dinghuo123.com/' + cleanUrl;
    },
    async getProducts(params = { page: 1, pageSize: 12, keyword: '' }) {
        return new Promise((resolve, reject) => {
            uni.request({
                url: `${BASE_URL}/api/products`,
                data: params,
                method: 'GET',
                success: (res) => {
                    if (res.statusCode === 200 && res.data.code === 200) {
                        const data = res.data.data;
                        const pageSize = params.pageSize || 12;
                        const currentPage = params.page || 1;
                        
                        // 添加调试日志
                        console.log('[API] getProducts response:', res.data);
                        
                        // 防守性检查：确保 list 存在
                        if (!data.list) {
                            console.warn('[API] data.list is undefined, initializing as empty array');
                            data.list = [];
                        }
                        
                        data.list = data.list.map(item => ({
                            ...item,
                            image: this.formatImageUrl(item.image),
                            memberPrice: this.calculateMemberPrice(item.purchasePrice)
                        }));
                        
                        // 添加分页信息便于前端判断
                        data.pageSize = pageSize;
                        data.page = currentPage;
                        data.total = data.total || 0;
                        data.hasMore = data.list.length >= pageSize && currentPage * pageSize < data.total;
                        
                        console.log('[API] processed data:', { list_count: data.list.length, total: data.total, hasMore: data.hasMore });
                        
                        resolve(data);
                    } else {
                        console.error('[API] Error response:', res.data);
                        reject(new Error(res.data.msg || '获取商品列表失败'));
                    }
                },
                fail: (err) => {
                    console.error('[API] getProducts failed:', err);
                    reject(err);
                }
            });
        });
    },
    async getProductDetail(id) {
        return new Promise((resolve, reject) => {
            uni.request({
                url: `${BASE_URL}/api/product/${id}`,
                method: 'GET',
                success: (res) => {
                    if (res.statusCode === 200 && res.data.code === 200) {
                        const product = res.data.data;
                        product.image = this.formatImageUrl(product.image);
                        if (product.album) {
                            product.album = product.album.map(img => this.formatImageUrl(img));
                        }
                        if (product.xcx_detail_images) {
                            product.xcx_detail_images = product.xcx_detail_images.map(img => this.formatImageUrl(img));
                        }
                        product.memberPrice = this.calculateMemberPrice(product.purchasePrice);
                        resolve(product);
                    } else {
                        reject(new Error(res.data.msg || '获取详情失败'));
                    }
                },
                fail: (err) => {
                    console.error('[API] getProductDetail failed:', err);
                    reject(err);
                }
            });
        });
    },
    async getHomeProducts(category = '全部') {
        const res = await this.getProducts({ page: 1, pageSize: 12, category: category });
        return res.list || [];
    },
    async getCategories() {
        return new Promise((resolve, reject) => {
            uni.request({
                url: `${BASE_URL}/api/categories`,
                method: 'GET',
                success: (res) => {
                    if (res.statusCode === 200 && res.data.code === 200) {
                        const data = res.data.data;
                        resolve(data);
                    } else {
                        // 降级到硬编码分类
                        resolve([
                            { name: '全部', id: 'all' },
                            { name: '水光', id: 'sg' },
                            { name: '面膜', id: 'mm' },
                            { name: '乔雅登', id: 'jyd' },
                            { name: '嗨体', id: 'ht' },
                            { name: '润致', id: 'rz' },
                            { name: '菲洛嘉', id: 'flg' }
                        ]);
                    }
                },
                fail: (err) => {
                    console.error('[API] getCategories failed:', err);
                    resolve([
                        { name: '全部', id: 'all' },
                        { name: '水光', id: 'sg' },
                        { name: '面膜', id: 'mm' },
                        { name: '乔雅登', id: 'jyd' },
                        { name: '嗨体', id: 'ht' },
                        { name: '润致', id: 'rz' },
                        { name: '菲洛嘉', id: 'flg' }
                    ]);
                }
            });
        });
    }
};
