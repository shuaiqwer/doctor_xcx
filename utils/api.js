/**
 * API 服务模块 - 生产环境对接版
 * 连接本地或生产环境后端，包含身份验证逻辑
 */

// 核心配置：根据反馈，本地开发请使用 localhost:8080
const BASE_URL = 'http://localhost:8080';
const API_KEY = 'admin-secret-key-123456';

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
        
        // 1. 标准化处理：转换为字符串并移除空白，统一斜杠
        let path = String(url).trim().replace(/\\/g, '/');
        
        const targetHost = 'oss.dinghuo123.com';
        const defaultBucket = 'images/productImage/';
        
        // 2. 如果已经包含 host，说明是全路径或包含域名的相对路径
        if (path.includes(targetHost)) {
            // 补全协议部分
            if (path.startsWith('//')) {
                path = 'https:' + path;
            } else if (!path.startsWith('http')) {
                // 如果是 oss.dinghuo123.com/... 格式，补上 https://
                path = 'https://' + path.substring(path.indexOf(targetHost));
            }
            
            // 检查是否存在重复的前缀堆叠情况 (例如 /images/productImage/images/productImage/)
            const doublePrefix = defaultBucket + defaultBucket;
            if (path.includes(doublePrefix)) {
                path = path.replace(new RegExp(doublePrefix, 'g'), defaultBucket);
            }
            return path;
        }
        
        // 3. 处理纯相对路径
        // 移除前导斜杠和各种干扰前缀
        if (path.startsWith('/')) path = path.substring(1);
        
        // 移除 Mock 数据路径干扰 (如 static/product_images/ 或 10位数字ID目录)
        path = path.replace(/^static\/product_images\/\d+\//, '');
        path = path.replace(/^product_images\/\d{8,}\//, '');
        
        // 如果路径已经包含 images/productImage/，则直接补全域名
        if (path.startsWith(defaultBucket)) {
            return `https://${targetHost}/${path}`;
        }
        
        // 如果是其他生产环境目录（如 product/detail/images/），也直接补全域名
        if (path.startsWith('product/')) {
            return `https://${targetHost}/${path}`;
        }
        
        // 其他情况（只有文件名或纯ID目录），拼接到默认 bucket 下
        return `https://${targetHost}/${defaultBucket}${path}`;
    },
    // 将后端复杂的结构标准化映射到前端需要的字段
    _mapProduct(item) {
        if (!item) return null;
        
        // 处理嵌套数组：item 为 [ {...} ] 的情况
        let actualItem = Array.isArray(item) ? item[0] : item;
        
        // 处理“商品信息”嵌套：优先读取键名为 "0" 的对象
        const info = actualItem['0'] || actualItem;

        // [提前处理] 解析可能存在的 JSON 字符串格式的相册数据
        let rawAlbumList = info.albumList || actualItem.albumList || info.AlbumList || info.imgList || [];
        if (typeof rawAlbumList === 'string' && rawAlbumList.startsWith('[')) {
            try { rawAlbumList = JSON.parse(rawAlbumList); } catch(e) { console.error('albumList parse error', e); }
        }
        
        let rawAlbum = info.album || actualItem.album || info.Album || actualItem.Album || [];
        if (typeof rawAlbum === 'string' && rawAlbum.startsWith('[')) {
            try { rawAlbum = JSON.parse(rawAlbum); } catch(e) { console.error('album parse error', e); }
        }
        
        // 1. 基础字段提取
        const rawPrice = parseFloat(info.orderPrice || actualItem.orderPrice || 0);
        
        // 主图逻辑强化：优先从各个可能的位置寻找带路径的图片
        const mainImgData = info.mainImg || info;
        const rawImg = info.imgUrl_480 || mainImgData.imgUrl_480 || 
                      info.imgUrl_cut || mainImgData.imgUrl_cut || 
                      info.imgUrl || mainImgData.imgUrl || 
                      info.image || mainImgData.image || 
                      info.img || mainImgData.img || 
                      actualItem.image || actualItem.img || '';
        
        // 提取业务目录 ID (如 2548203/)，用于修复内容中缺失目录的文件名
        let businessFolder = '';
        const extractFolder = (str) => {
            if (!str || typeof str !== 'string') return '';
            // 匹配格式如 "2548203/..." 或者 "productImage/2548203/..."
            const match = str.match(/(?:^|\/)(\d{5,8})\//);
            return match ? match[1] + '/' : '';
        };

        businessFolder = extractFolder(rawImg);
        
        // 如果主图没提取到目录，尝试从相册第一个或原始数据中提取
        if (!businessFolder && Array.isArray(rawAlbumList) && rawAlbumList.length > 0) {
            const first = rawAlbumList[0];
            const str = (typeof first === 'object') ? (first.imgUrl_480 || first.imgUrl_cut || first.imgUrl || '') : first;
            businessFolder = extractFolder(str);
        }
        
        // 兜底：检查 info 对象里的 ID 字段
        if (!businessFolder && info.dbid) {
            businessFolder = info.dbid + '/';
        }
        
        // 2. 构造对象并初步拼接路径
        const processedProduct = {
            ...actualItem,
            ...info,
            id: info.id || actualItem.id,
            name: info.name || actualItem.name,
            price: rawPrice,
            image: this.formatImageUrl(rawImg),
            memberPrice: info.memberPrice || this.calculateMemberPrice(rawPrice),
            brand: info.brand || actualItem.brand || '精品严选',
            stock: info.inventoryCount || info.stock || 0,
            unit: info.productUnitName || info.unit || '件',
            code: info.code || actualItem.code || '',
            originalPrice: (info.unitList && info.unitList[0]) ? info.unitList[0].marketPrice : (info.marketPrice || rawPrice),
            desc: info.remark || info.description_brief || info.description || '官方正品，质量保障',
            detailHtml: info.description || info.content || info.detailHtml || ''
        };
        
        // 3. 处理轮播图 (Album)
        let album = [];
        if (Array.isArray(rawAlbumList) && rawAlbumList.length > 0) {
            album = rawAlbumList.map(i => {
                let imgStr = (typeof i === 'object') ? (i.imgUrl_480 || i.imgUrl_cut || i.imgUrl || '') : i;
                if (imgStr && !imgStr.includes('/') && businessFolder) imgStr = businessFolder + imgStr;
                return this.formatImageUrl(imgStr);
            });
        } else if (Array.isArray(rawAlbum) && rawAlbum.length > 0) {
            album = rawAlbum.map(img => {
                let imgStr = (typeof img === 'object') ? (img.imgUrl || img.url || '') : img;
                if (imgStr && !imgStr.includes('/') && businessFolder) imgStr = businessFolder + imgStr;
                return this.formatImageUrl(imgStr);
            });
        }
        
        // [关键对齐] 同步主图：如果轮播图有内容，且主图链接看起来不够完整，则强制使用相册第一张
        if (album.length > 0) {
            const firstAlbumImg = album[0];
            const currentMain = processedProduct.image || '';
            
            // 下列场景下强制替换主图为相册首图：
            // 1. 主图为空
            // 2. 相册首图包含裁剪处理参数(@)，而当前主图不包含
            // 3. 相册首图路径包含业务目录(/), 而当前主图只剩个文件名
            // 4. 相册首图包含 @480w，而主图只包含较小的 @200w 或 @60w
            const isBetter = (!currentMain) || 
                             (firstAlbumImg.includes('@') && !currentMain.includes('@')) ||
                             (firstAlbumImg.includes('/') && !currentMain.includes('/')) ||
                             (firstAlbumImg.includes('@480w') && currentMain.includes('@200w'));

            if (isBetter) {
                processedProduct.image = firstAlbumImg;
            }
        }
        
        // 兜底逻辑
        processedProduct.album = album.length > 0 ? album : [processedProduct.image];
        processedProduct.albumlist = processedProduct.album;
        
        // 5. 详情图处理
        if (processedProduct.xcx_detail_images || processedProduct.XcxDetailImages) {
            const detailImgs = processedProduct.xcx_detail_images || processedProduct.XcxDetailImages;
            processedProduct.xcx_detail_images = detailImgs.map(img => this.formatImageUrl(img.imgUrl || img));
        }
        
        return processedProduct;
    },
    async getProducts(params = { page: 1, pageSize: 12, keyword: '' }) {
        const queryData = {
            ...params,
            key: API_KEY
        };
        const requestUrl = `${BASE_URL}/api/v1/products`;
        
        return new Promise((resolve, reject) => {
            uni.request({
                url: requestUrl,
                data: queryData,
                method: 'GET',
                success: (res) => {
                    if (res.statusCode === 200) {
                        let data = res.data;
                        if (typeof data === 'string') {
                            try { data = JSON.parse(data); } catch (e) {}
                        }
                        
                        console.log('[API] 接口返回原始数据:', data);
                        
                        // 1. 获取列表
                        const result = data.data || data;
                        const list = result.items || result.list || [];
                        const totalCount = result.totalCount || result.total || 0;
                        
                        // 2. 深度处理每一个商品项
                        const processedList = list.map(item => apiService._mapProduct(item));

                        resolve({
                            list: processedList,
                            total: totalCount,
                            pageSize: params.pageSize,
                            page: params.page
                        });
                    } else {
                        reject(new Error(`请求失败: ${res.statusCode}`));
                    }
                },
                fail: (err) => reject(err)
            });
        });
    },
    async getProductDetail(id) {
        return new Promise((resolve, reject) => {
            const requestUrl = `${BASE_URL}/api/v1/product-details/${id}`;
            uni.request({
                url: requestUrl,
                data: { key: API_KEY },
                method: 'GET',
                success: (res) => {
                    if (res.statusCode === 200 || res.statusCode === 201) {
                        let data = res.data;
                        if (typeof data === 'string') {
                            try { data = JSON.parse(data); } catch(e) {}
                        }
                        
                        const product = data.data || data;
                        const processedProduct = apiService._mapProduct(product);
                        
                        resolve(processedProduct);
                    } else {
                        reject(new Error(`详情获取失败: ${res.statusCode}`));
                    }
                },
                fail: (err) => reject(err)
            });
        });
    },
    async getHomeProducts(category = '全部') {
        const params = { page: 1, pageSize: 12 };
        // 如果是 '全部'，则不向后端发送 category 过滤参数，以获取全量数据
        if (category && category !== '全部' && category !== 'all') {
            params.category = category;
        }
        const res = await apiService.getProducts(params);
        return res.list || [];
    },
    async getCategories() {
        return new Promise((resolve, reject) => {
            uni.request({
                url: `${BASE_URL}/api/v1/brands`,
                data: { key: API_KEY },
                method: 'GET',
                success: (res) => {
                    console.log('[API] Brands raw response:', res.statusCode);
                    if (res.statusCode === 200 || res.data.code === 200 || res.data.Code === 0) {
                        let data = res.data;
                        if (typeof data === 'string') {
                            try { data = JSON.parse(data); } catch(e) {}
                        }
                        
                        const d = data.data || data.Data || data;
                        const rawList = Array.isArray(d) ? d : (d.list || d.List || d.rows || d.Rows || []);
                        
                        // 标准化为对象列表 [{name, id}]
                        const list = rawList.map(item => {
                            if (typeof item === 'string') {
                                return { name: item, id: item };
                            }
                            const name = item.name || item.Name || item.brandName || item.BrandName || '未知分类';
                            const id = item.id || item.ID || item.Id || name || '';
                            return { name, id };
                        });
                        
                        resolve(list);
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
    },

    // --- 用户与身份认证 ---
    
    /**
     * 实现自动登录或凭包获取的参数登录
     */
    async autoLogin() {
        const openId = uni.getStorageSync('debug_openId');
        const userName = uni.getStorageSync('debug_userName');
        
        if (!openId) throw new Error('未检测到 OpenID，请先前往登录页设置');

        return new Promise((resolve, reject) => {
            uni.request({
                url: `${BASE_URL}/api/v1/user/login`,
                method: 'POST',
                data: {
                    openId,
                    userName,
                    key: API_KEY
                },
                success: (res) => {
                    if (res.statusCode === 200 && res.data.token) {
                        uni.setStorageSync('token', res.data.token);
                        uni.setStorageSync('userInfo', res.data.user || {});
                        resolve(res.data.token);
                    } else {
                        reject(new Error(res.data.message || '登录授权失败'));
                    }
                },
                fail: (err) => reject(err)
            });
        });
    },

    /**
     * 获取用户信息
     */
    async getUserInfo() {
        return this._authorizedRequest({
            url: `${BASE_URL}/api/v1/user/profile`,
            method: 'GET'
        });
    },

    // --- 订单与库存储管理 ---

    /**
     * 获取订单列表
     */
    async getOrders(status = 'all') {
        return this._authorizedRequest({
            url: `${BASE_URL}/api/v1/orders`,
            method: 'GET',
            data: { status }
        });
    },

    /**
     * 提交订单
     */
    async submitOrder(orderData) {
        return this._authorizedRequest({
            url: `${BASE_URL}/api/v1/orders/create`,
            method: 'POST',
            data: orderData
        });
    },

    /**
     * 内部辅助方法：处理带 Token 的请求
     */
    async _authorizedRequest(options) {
        const token = uni.getStorageSync('token');
        if (!token) {
            // 引导去登录
            uni.navigateTo({ url: '/pages/login/login' });
            return Promise.reject(new Error('Unauthorized'));
        }

        return new Promise((resolve, reject) => {
            uni.request({
                ...options,
                header: {
                    ...options.header,
                    'Authorization': `Bearer ${token}`
                },
                data: {
                    ...options.data,
                    key: API_KEY
                },
                success: (res) => {
                    if (res.statusCode === 401) {
                        uni.removeStorageSync('token');
                        uni.navigateTo({ url: '/pages/login/login' });
                        reject(new Error('Token 过期'));
                    } else if (res.statusCode >= 200 && res.statusCode < 300) {
                        resolve(res.data.data || res.data);
                    } else {
                        reject(new Error(res.data.message || '请求失败'));
                    }
                },
                fail: (err) => reject(err)
            });
        });
    }
};

