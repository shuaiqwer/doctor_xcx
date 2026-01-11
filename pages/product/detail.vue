<template>
	<view class="container">
		<!-- 商品图片展示区域 (仿照设计图) -->
		<view class="image-gallery">
			<!-- 主图显示 -->
			<view class="main-image-wrapper">
				<image 
					:src="product.albumlist[currentImgIndex] || product.image" 
					mode="aspectFit" 
					class="main-image" 
					referrer-policy="no-referrer"
					@error="onMainImgError"
				></image>
			</view>
			
			<!-- 缩略图轮播列表 -->
			<view class="thumb-scroller-wrapper">
				<view class="nav-arrow left" @click="prevThumb" v-if="product.albumlist && product.albumlist.length > 4">
					<text class="arrow-icon">‹</text>
				</view>
				
				<scroll-view class="thumb-list" scroll-x :scroll-into-view="'thumb-' + currentImgIndex" scroll-with-animation>
					<view 
						class="thumb-item" 
						v-for="(img, index) in product.albumlist" 
						:key="index"
						:id="'thumb-' + index"
						:class="{ active: currentImgIndex === index }"
						@click="currentImgIndex = index"
					>
						<image :src="img" mode="aspectFill" class="thumb-image" referrer-policy="no-referrer"></image>
					</view>
				</scroll-view>
				
				<view class="nav-arrow right" @click="nextThumb" v-if="product.albumlist && product.albumlist.length > 4">
					<text class="arrow-icon">›</text>
				</view>
			</view>
		</view>

		<!-- 分段选项卡 (仿照设计图) -->
		<view class="tab-header">
			<view class="tab-item" :class="{ active: currentTab === 0 }" @click="currentTab = 0">
				<text class="tab-text">商品介绍</text>
				<view class="tab-line" v-if="currentTab === 0"></view>
			</view>
			<view class="tab-item" :class="{ active: currentTab === 1 }" @click="currentTab = 1">
				<text class="tab-text">商品附件</text>
				<view class="tab-line" v-if="currentTab === 1"></view>
			</view>
		</view>

		<!-- 商品基本信息 -->
		<view class="info-section">
			<view class="price-row">
				<view class="main-price">
					<text class="currency">￥</text>
					<text class="price">{{product.price}}</text>
				</view>
				<view class="luxury-member-badge" :style="{ background: memberLevel.bg, color: memberLevel.textColor, border: memberLevel.border }">
					<text class="m-label">{{memberLevel.name}}价</text>
					<text class="m-price">￥{{product.memberPrice}}</text>
				</view>
				<text class="original-price">￥{{product.originalPrice}}</text>
			</view>
			<view class="title-row">
				<view class="brand-tag">{{product.brand}}</view>
				<text class="product-title">{{product.name}}</text>
				
			</view>
			
			<!-- 规格参数简述 -->
			<view class="spec-brief">
				<view class="spec-item">
					<text class="label">库存</text>
					<text class="value">{{product.stock}}{{product.unit}}</text>
				</view>
				<view class="spec-item">
					<text class="label">编号</text>
					<text class="value">{{product.code}}</text>
				</view>
				<view class="spec-item">
					<text class="label">单位</text>
					<text class="value">{{product.unit}}</text>
				</view>
			</view>
		</view>

		<!-- 权威保障 -->
		<view class="trust-section">
			<view class="trust-item">
				<icon type="success" size="14" color="#D4AF37" />
				<text>正品保障</text>
			</view>
			<view class="trust-item">
				<icon type="success" size="14" color="#D4AF37" />
				<text>药监备案</text>
			</view>
			<view class="trust-item">
				<icon type="success" size="14" color="#D4AF37" />
				<text>极速发货</text>
			</view>
			<view class="trust-item">
				<icon type="success" size="14" color="#D4AF37" />
				<text>售后无忧</text>
			</view>
		</view>

		<!-- 会员引导 -->
		<view class="member-guide" @click="goToMember">
			<view class="guide-left">
				<text class="gold-text">{{memberLevel.name}}尊享优惠，当前已省￥{{(product.price - product.memberPrice).toFixed(2)}}</text>
			</view>
			<view class="guide-right">
				<text>查看权益 ></text>
			</view>
		</view>

		<!-- 商品详情图 -->
		<view class="detail-section" v-if="currentTab === 0">
			<view class="section-title">
				<text class="title-text">商品详情</text>
				<view class="title-line"></view>
			</view>
			<view class="detail-content">
				<!-- 混合模式渲染：文本用 rich-text，图片用原生 image 组件 -->
				<block v-if="splitNodes && splitNodes.length > 0">
					<block v-for="(node, index) in splitNodes" :key="index">
						<!-- 文本段落 -->
						<rich-text v-if="node.type === 'html'" :nodes="node.content"></rich-text>
						<!-- 原生图片 -->
						<image 
							v-else-if="node.type === 'img'" 
							:src="node.src" 
							mode="widthFix" 
							style="width: 100%; display: block;"
							lazy-load
							@error="onImgError($event, index)"
							@load="onImgLoad($event, index)"
						></image>
					</block>
				</block>
                <!-- 加载失败或无内容提示 -->
				<view v-else class="no-detail">
					<view class="detail-img-placeholder" style="height: 600rpx;"></view>
					<text class="placeholder-text">正品保障 · 药监备案 · 官方直供</text>
					<view class="detail-img-placeholder" style="height: 800rpx; margin-top: 20rpx;"></view>
				</view>
			</view>
		</view>

		<!-- 底部操作栏 -->
		<view class="footer-bar">
			<view class="icon-btns">
				<view class="icon-item" @click="showToast('联系客服')">
					<icon type="contact" size="20" color="#7F8C8D" />
					<text>客服</text>
				</view>
				<view class="icon-item" @click="showToast('收藏成功')">
					<icon type="star" size="20" color="#7F8C8D" />
					<text>收藏</text>
				</view>
			</view>
			<view class="action-btns">
				<view class="cart-btn" @click="addToCart">加入购物车</view>
				<view class="buy-btn" @click="buyNow">立即购买</view>
			</view>
		</view>
	</view>
</template>

<script>
	import { apiService, MEMBER_LEVELS } from '@/utils/api.js';

	export default {
		data() {
			return {
				productId: '',
                currentImgIndex: 0,
                currentTab: 0,
                splitNodes: [], // 用于存储拆分后的图文节点
				product: {
					name: '加载中...',
					price: '0.00',
					originalPrice: '0.00',
					memberPrice: '0.00',
                    album: [],
                    albumlist: [],
					desc: '正品保障，药监局合规备案，冷链直发。'
				},
				memberLevel: {}
			}
		},
		async onLoad(options) {
			this.productId = options.id;
			const levelKey = apiService.getCurrentMemberLevel();
			this.memberLevel = MEMBER_LEVELS[levelKey];
			await this.loadProductDetail();
		},
		methods: {
			parseDetailHtml(html, localizedImages = []) {
                if (!html) return [];
                const nodes = [];
                // 1. 基础清洗HTML entities
                let cleanHtml = html.replace(/\\/g, '')
                    .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
                    .replace(/&#60;/g, '<').replace(/&#62;/g, '>')
                    .replace(/&#34;/g, '"').replace(/&quot;/g, '"');
                
                let lastIndex = 0;
                // [优化] 更强大的正则：支持各种属性顺序，并兼容 data-src
                const imgRegex = /<img[^>]*>/gi;
                let match;
                let imgCount = 0;
                
                while ((match = imgRegex.exec(cleanHtml)) !== null) {
                    const imgTag = match[0];
                    // 添加图片前面的文本
                    if (match.index > lastIndex) {
                        const textPart = cleanHtml.substring(lastIndex, match.index);
                        if (textPart.trim()) {
                            nodes.push({ type: 'html', content: this.formatRichText(textPart, false) });
                        }
                    }
                    
                    // 提取 src 或 data-src (备选)
                    let src = '';
                    const srcM = imgTag.match(/src\s*=\s*(['"]?)([^'"\s>]+)\1/i);
                    const dsM = imgTag.match(/data-src\s*=\s*(['"]?)([^'"\s>]+)\1/i);
                    
                    src = (srcM && srcM[2] && srcM[2].length > 5) ? srcM[2] : 
                          ((dsM && dsM[2]) ? dsM[2] : '');
                    
                    // [逻辑优化] 优先使用 HTML 中的原始地址。如果地址无效，则使用备份
                    if ((!src || src.length < 5) && localizedImages && localizedImages[imgCount]) {
                        src = localizedImages[imgCount];
                    }
                    
                    // 统一处理路径
                    src = apiService.formatImageUrl(src);
                    
                    // 添加图片节点
                    if (src) {
                        nodes.push({ type: 'img', src: src });
                    }
                    
                    lastIndex = imgRegex.lastIndex;
                    imgCount++;
                }
                
                // 添加剩余文本
                if (lastIndex < cleanHtml.length) {
                    const textPart = cleanHtml.substring(lastIndex);
                    if (textPart.trim()) {
                        nodes.push({ type: 'html', content: this.formatRichText(textPart, false) });
                    }
                }
                
                if (nodes.length === 0 && cleanHtml) {
                     nodes.push({ type: 'html', content: this.formatRichText(cleanHtml, false) });
                }
                
                return nodes;
            },
			formatRichText(html, processImg = true) {
				if (!html) return '';
				
				// 1. 基础清洗
				let newHtml = html.replace(/\\/g, '');
				
                if (processImg) {
                    // 2. 移除原有的 img 标签，重构为标准标签 (保留给兜底逻辑用)
                    newHtml = newHtml.replace(/<img[^>]*>/gi, function(match) {
                        var srcMatch = match.match(/src\s*=\s*(['"]?)([^'"\s>]+)\1/i);
                        var src = srcMatch ? srcMatch[2] : '';
                        if (!src) return '';
                        
                        // 统一使用 apiService 的格式化方法
                        src = apiService.formatImageUrl(src);
                        
                        return `<img src="${src}" width="100%" class="rich-img" style="width:100%; height:auto; display:block; margin-bottom:10px;" referrer-policy="no-referrer" />`;
                    });
                }
				
				// 4. 段落优化
				newHtml = newHtml.replace(/<p[^>]*>/gi, '<p class="rich-p" style="margin:0; padding:0; line-height:1.6;">');
				
				return newHtml;
			},
            onImgError(e, index) {
                console.error('Image load error at index ' + index, e);
            },
            onMainImgError(e) {
                const url = this.product.albumlist[this.currentImgIndex] || this.product.image;
                console.error('[IMAGE ERROR] 主图加载失败:', url, e);
            },
            onImgLoad(e, index) {
                // 图片加载成功，可以在这里处理占位图隐藏等逻辑
                // console.log('Image loaded at index ' + index);
            },
            prevThumb() {
                if (this.currentImgIndex > 0) {
                    this.currentImgIndex--;
                } else if (this.product.albumlist && this.product.albumlist.length > 0) {
                    this.currentImgIndex = this.product.albumlist.length - 1;
                }
            },
            nextThumb() {
                if (this.product.albumlist && this.currentImgIndex < this.product.albumlist.length - 1) {
                    this.currentImgIndex++;
                } else {
                    this.currentImgIndex = 0;
                }
            },
			async loadProductDetail() {
				try {
					// 优先获取完整详情
					const detail = await apiService.getProductDetail(this.productId);
					this.product = detail; // apiService 已经处理过图片和价格了
                    this.currentImgIndex = 0; // 重置索引

                    if (this.productId == '1042777132') {
                        console.log('[DEBUG-DETAIL] productId=1042777132 原始详情对象:', JSON.stringify(detail));
                        console.log('[DEBUG-DETAIL] 映射后主图:', this.product.image);
                        console.log('[DEBUG-DETAIL] 映射后相册:', this.product.albumlist);
                    }
                    
                    console.log('[DEBUG] 商品主图 URL:', this.product.image);
                    console.log('[DEBUG] 商品轮播图内容:', this.product.album);
                    
                    this.splitNodes = this.parseDetailHtml(this.product.detailHtml, detail.xcx_detail_images || []);
                    console.log('[DEBUG] Final splitNodes count:', this.splitNodes.length);
				} catch (e) {
					console.warn('获取完整详情失败，尝试从列表数据加载', e);
					// 降级方案：从列表数据中找
					try {
						const res = await apiService.getProducts({ page: 1, pageSize: 2000 });
						const found = res.list.find(p => p.id == this.productId);
						if (found) {
							this.product = found;
                            
                            this.splitNodes = this.parseDetailHtml(this.product.detailHtml, found.xcx_detail_images || []);
						}
					} catch (err) {
						console.error('加载详情失败', err);
					}
				}
			},
			goToConfirm() {
				uni.navigateTo({
					url: '/pages/order/confirm'
				});
			},
			goToMember() {
				uni.navigateTo({
					url: '/pages/mine/member'
				});
			},
			addToCart() {
				const cart = uni.getStorageSync('cart') || [];
				const index = cart.findIndex(item => item.id === this.product.id);
				
				if (index > -1) {
					cart[index].count += 1;
				} else {
					cart.push({
						id: this.product.id,
						name: this.product.name,
						image: this.product.image,
						price: this.product.memberPrice, // 使用会员价
						originalPrice: this.product.price,
						count: 1,
						selected: true
					});
				}
				
				uni.setStorageSync('cart', cart);
				uni.showToast({ title: '已加入购物车', icon: 'success' });
			},
			buyNow() {
				// 立即购买通常通过 URL 参数传递购买内容，或者存入临时变量
				const orderItem = {
					id: this.product.id,
					name: this.product.name,
					image: this.product.image,
					price: this.product.memberPrice,
					count: 1
				};
				uni.setStorageSync('temp_order_items', [orderItem]);
				uni.navigateTo({
					url: '/pages/order/confirm?from=buyNow'
				});
			},
			showToast(msg) {
				uni.showToast({
					title: msg,
					icon: 'none'
				});
			}
		}
	}
</script>

<style lang="scss">
	.container {
		background-color: #F4F7F6;
		padding-bottom: 120rpx;
		min-height: 100vh;
	}

	.image-gallery {
		background-color: #fff;
		padding: 20rpx;
		
		.main-image-wrapper {
			width: 100%;
			height: 600rpx;
			display: flex;
			justify-content: center;
			align-items: center;
			margin-bottom: 20rpx;
			
			.main-image {
				width: 100%;
				height: 100%;
				background-color: #fff;
			}
		}
		
		.thumb-scroller-wrapper {
			display: flex;
			align-items: center;
			padding: 0 10rpx;
			position: relative;
			
			.nav-arrow {
				width: 40rpx;
				height: 80rpx;
				display: flex;
				justify-content: center;
				align-items: center;
				background-color: rgba(255,255,255,0.8);
				z-index: 10;
				
				.arrow-icon {
					font-size: 40rpx;
					color: #999;
				}
				
				&.left { margin-right: 10rpx; }
				&.right { margin-left: 10rpx; }
			}
			
			.thumb-list {
				flex: 1;
				white-space: nowrap;
				height: 110rpx;
				
				.thumb-item {
					display: inline-block;
					width: 100rpx;
					height: 100rpx;
					margin-right: 20rpx;
					border: 4rpx solid transparent;
					box-sizing: border-box;
					
					&.active {
						border-color: #00bcd4; // 设计图中的青色边框
					}
					
					.thumb-image {
						width: 100%;
						height: 100%;
					}
				}
			}
		}
	}

	.tab-header {
		display: flex;
		background-color: #fff;
		border-top: 1rpx solid #eee;
		border-bottom: 1rpx solid #eee;
		margin-top: 20rpx;
		
		.tab-item {
			flex: 1;
			height: 90rpx;
			display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;
			position: relative;
			
			.tab-text {
				font-size: 28rpx;
				color: #666;
			}
			
			&.active {
				.tab-text {
					color: #00bcd4;
					font-weight: bold;
				}
			}
			
			.tab-line {
				position: absolute;
				bottom: 0;
				width: 140rpx;
				height: 4rpx;
				background-color: #00bcd4;
			}
		}
	}

	.info-section {
		background-color: #fff;
		padding: 30rpx;
		margin-bottom: 20rpx;
		
		.price-row {
			display: flex;
			align-items: center;
			margin-bottom: 20rpx;
			flex-wrap: wrap;
			
			.main-price {
				display: flex;
				align-items: baseline;
				margin-right: 20rpx;
				.currency { font-size: 32rpx; color: #E74C3C; font-weight: bold; }
				.price { font-size: 56rpx; color: #E74C3C; font-weight: bold; }
			}
			
			.luxury-member-badge {
				border-radius: 40rpx;
				display: flex;
				align-items: center;
				padding: 6rpx 24rpx;
				margin-right: 20rpx;
				box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.15);
				
				.m-label {
					font-size: 20rpx;
					font-weight: bold;
					margin-right: 12rpx;
				}
				
				.m-price {
					font-size: 28rpx;
					font-weight: bold;
				}
			}
			
			.original-price { font-size: 26rpx; color: #BDC3C7; text-decoration: line-through; }
		}
		
		.title-row {
			display: flex;
			align-items: flex-start;
			margin-bottom: 15rpx;
			.brand-tag {
				background-color: #2C3E50;
				color: #fff;
				font-size: 20rpx;
				padding: 4rpx 12rpx;
				border-radius: 4rpx;
				margin-right: 15rpx;
				white-space: nowrap;
				margin-top: 6rpx;
			}
			.product-title {
				font-size: 34rpx;
				color: #2C3E50;
				font-weight: bold;
				line-height: 48rpx;
			}
		}
		
		.desc-text {
			font-size: 26rpx;
			color: #7F8C8D;
			line-height: 40rpx;
			margin-bottom: 30rpx;
		}

		.spec-brief {
			display: flex;
			background-color: #F8F9F9;
			padding: 20rpx;
			border-radius: 12rpx;
			
			.spec-item {
				flex: 1;
				display: flex;
				flex-direction: column;
				align-items: center;
				border-right: 1rpx solid #EBEEF5;
				
				&:last-child {
					border-right: none;
				}
				
				.label {
					font-size: 20rpx;
					color: #BDC3C7;
					margin-bottom: 8rpx;
				}
				
				.value {
					font-size: 24rpx;
					color: #2C3E50;
					font-weight: 500;
				}
			}
		}
	}

	.trust-section {
		background-color: #fff;
		padding: 20rpx 30rpx;
		display: flex;
		justify-content: space-between;
		margin-bottom: 20rpx;
		.trust-item {
			display: flex;
			align-items: center;
			text { font-size: 22rpx; color: #7F8C8D; margin-left: 8rpx; }
		}
	}

	.member-guide {
		margin: 0 20rpx 20rpx;
		background: linear-gradient(90deg, #3D3D3D 0%, #1A1A1A 100%);
		border-radius: 12rpx;
		padding: 20rpx 30rpx;
		display: flex;
		justify-content: space-between;
		align-items: center;
		
		.gold-text {
			font-size: 26rpx;
			color: #D4AF37;
			font-weight: bold;
		}
		
		.guide-right {
			font-size: 22rpx;
			color: #D4AF37;
		}
	}

	.detail-section {
		background-color: #fff;
		padding: 40rpx 0;
		
		.section-title {
			display: flex;
			flex-direction: column;
			align-items: center;
			margin-bottom: 40rpx;
			
			.title-text {
				font-size: 32rpx;
				font-weight: bold;
				color: #2C3E50;
				letter-spacing: 4rpx;
			}
			
			.title-line {
				width: 40rpx;
				height: 4rpx;
				background-color: #D4AF37;
				margin-top: 10rpx;
				border-radius: 2rpx;
			}
		}
		
		.detail-content {
			padding: 0 20rpx;
			
			:deep(img) {
				max-width: 100%;
				height: auto;
				display: block;
				margin: 0 auto;
			}

			.no-detail {
				display: flex;
				flex-direction: column;
				align-items: center;
				
				.placeholder-text {
					font-size: 24rpx;
					color: #BDC3C7;
					margin: 40rpx 0;
				}
			}
		}
		
		.detail-img-placeholder {
			width: 100%;
			background-color: #F8F9F9;
			border-radius: 12rpx;
		}
	}

	.footer-bar {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		height: 110rpx;
		background-color: #fff;
		display: flex;
		align-items: center;
		padding: 0 30rpx;
		padding-bottom: env(safe-area-inset-bottom);
		box-shadow: 0 -4rpx 20rpx rgba(0,0,0,0.05);
		z-index: 100;
		
		.icon-btns {
			display: flex;
			margin-right: 30rpx;
			
			.icon-item {
				display: flex;
				flex-direction: column;
				align-items: center;
				margin-right: 40rpx;
				
				text {
					font-size: 20rpx;
					color: #7F8C8D;
					margin-top: 6rpx;
				}
			}
		}
		
		.action-btns {
			flex: 1;
			display: flex;
			height: 80rpx;
			
			.cart-btn {
				flex: 1;
				background-color: #2C3E50;
				color: #fff;
				display: flex;
				align-items: center;
				justify-content: center;
				font-size: 28rpx;
				border-top-left-radius: 40rpx;
				border-bottom-left-radius: 40rpx;
			}
			
			.buy-btn {
				flex: 1;
				background: linear-gradient(to right, #D4AF37, #B8860B);
				color: #fff;
				display: flex;
				align-items: center;
				justify-content: center;
				font-size: 28rpx;
				font-weight: bold;
				border-top-right-radius: 40rpx;
				border-bottom-right-radius: 40rpx;
			}
		}
	}
        
        /* 解决小程序 img 标签选择器失效问题，改为 class 选择器 */
        .rich-img {
            max-width: 100% !important;
            width: 100% !important;
            height: auto !important;
            display: block !important;
        }
</style>
