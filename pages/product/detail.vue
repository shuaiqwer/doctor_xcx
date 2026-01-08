<template>
	<view class="container">
		<!-- 商品图片轮播 -->
		<swiper class="product-banner" indicator-dots autoplay circular indicator-active-color="#D4AF37">
			<swiper-item v-for="(img, index) in product.album" :key="index">
				<image :src="img" mode="aspectFill" class="banner-image" referrer-policy="no-referrer"></image>
			</swiper-item>
			<swiper-item v-if="!product.album || product.album.length === 0">
				<image :src="product.image" mode="aspectFill" class="banner-image" referrer-policy="no-referrer"></image>
			</swiper-item>
		</swiper>

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
			<view class="desc-text">{{product.desc}}</view>
			
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
		<view class="detail-section">
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
				<view class="cart-btn" @click="showToast('已加入购物车')">加入购物车</view>
				<view class="buy-btn" @click="goToConfirm">立即购买</view>
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
                splitNodes: [], // 用于存储拆分后的图文节点
				product: {
					name: '加载中...',
					price: '0.00',
					originalPrice: '0.00',
					memberPrice: '0.00',
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
                // [修复] 允许 src 为空的情况 (把 + 改为 *)
                const imgRegex = /<img[^>]*src\s*=\s*['"]([^'"]*)['"][^>]*>/gi;
                let match;
                let imgCount = 0;
                
                console.log('[DEBUG] Parsing HTML length:', cleanHtml.length);
                console.log('[DEBUG] Localized images count:', localizedImages ? localizedImages.length : 0);
                
                while ((match = imgRegex.exec(cleanHtml)) !== null) {
                    // 添加图片前面的文本
                    if (match.index > lastIndex) {
                        const textPart = cleanHtml.substring(lastIndex, match.index);
                        if (textPart.trim()) {
                            nodes.push({ type: 'html', content: this.formatRichText(textPart, false) });
                        }
                    }
                    
                    // 提取图片 src
                    let src = match[1];
                    
                    // [关键修复] 如果有本地化图片，优先使用对应的
                    if (localizedImages && localizedImages[imgCount]) {
                        src = localizedImages[imgCount];
                    }
                    
                    // 统一处理路径
                    src = apiService.formatImageUrl(src);
                    
                    // 添加图片节点
                    nodes.push({ type: 'img', src: src });
                    
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
                        var srcMatch = match.match(/src\s*=\s*['"]([^'"]+)['"]/i);
                        if (!srcMatch) srcMatch = match.match(/src\s*=\s*([^ >]+)/i);
                        var src = srcMatch ? srcMatch[1] : '';
                        if (!src) return '';
                        if (src.indexOf('//') === 0) src = 'https:' + src;
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
            onImgLoad(e, index) {
                // 图片加载成功，可以在这里处理占位图隐藏等逻辑
                // console.log('Image loaded at index ' + index);
            },
			async loadProductDetail() {
				try {
					// 优先获取完整详情
					const detail = await apiService.getProductDetail(this.productId);
					this.product = {
						...detail,
					memberPrice: apiService.calculateMemberPrice(detail.purchasePrice)
				};
                    
                    this.splitNodes = this.parseDetailHtml(this.product.detailHtml, detail.xcx_detail_images || []);
                    console.log('[DEBUG] Final splitNodes count:', this.splitNodes.length);
				} catch (e) {
					console.warn('获取完整详情失败，尝试从列表数据加载', e);
					// 降级方案：从列表数据中找
					try {
						const res = await apiService.getProducts({ page: 1, pageSize: 2000 });
						const found = res.list.find(p => p.id == this.productId);
						if (found) {
							this.product = {
								...found,
							memberPrice: apiService.calculateMemberPrice(found.purchasePrice),
							};
                            
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

	.product-banner {
		height: 750rpx;
		background-color: #fff;
		
		.banner-image {
			width: 100%;
			height: 100%;
		}
		
		.banner-img-placeholder {
			width: 100%;
			height: 100%;
			background-color: #F8F9F9;
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
				border-radius: 8rpx;
				display: flex;
				align-items: center;
				padding: 6rpx 16rpx;
				margin-right: 20rpx;
				box-shadow: 0 4rpx 8rpx rgba(0,0,0,0.15);
				
				.m-label {
					font-size: 20rpx;
					font-weight: bold;
					margin-right: 10rpx;
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
