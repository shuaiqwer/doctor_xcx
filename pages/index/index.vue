<template>
	<view class="container">
		<!-- 顶部状态栏占位 -->
		<view class="status-bar"></view>
		
		<!-- 权威认证背书栏 -->
		<view class="trust-header">
			<view class="trust-item">
				<icon type="success" size="12" color="#D4AF37" />
				<text>药监局备案</text>
			</view>
			<view class="trust-item">
				<icon type="success" size="12" color="#D4AF37" />
				<text>正品溯源</text>
			</view>
			<view class="trust-item">
				<icon type="success" size="12" color="#D4AF37" />
				<text>冷链直达</text>
			</view>
		</view>

		<!-- 搜索栏 -->
		<view class="search-bar" @click="goToSearch()">
			<view class="search-input">
				<icon type="search" size="16" color="#7F8C8D" />
				<text class="placeholder">搜索全球正品美容药品</text>
			</view>
		</view>

		<!-- 轮播图 -->
		<swiper class="banner" indicator-dots autoplay circular interval="4000" indicator-active-color="#D4AF37">
			<swiper-item v-for="(item, index) in banners" :key="index" @click="goToDetail(item)">
				<view class="banner-card">
					<view class="banner-content" :style="{ background: item.gradient }">
						<view class="banner-tag">官方直供</view>
						<text class="banner-title">{{item.title}}</text>
						<text class="banner-subtitle">{{item.subtitle}}</text>
					</view>
				</view>
			</swiper-item>
		</swiper>

		<!-- 核心分类 -->
		<view class="category-section">
			<view class="category-grid">
				<view class="category-item" v-for="(item, index) in categories" :key="index" @click="goToCategory(item)">
					<view class="category-icon-wrapper">
						<view class="category-icon" :style="{ background: item.gradient || '#EBF5FB' }">
							<text class="cat-initial">{{item.name.substring(0,1)}}</text>
						</view>
					</view>
					<text class="category-name">{{item.name}}</text>
				</view>
			</view>
		</view>

		<!-- 快捷功能区 -->
		<view class="quick-actions">
			<view class="action-item" @click="goToCategory({name: '水光'})">
				<view class="action-icon hot">🔥</view>
				<text>爆款水光</text>
			</view>
			<view class="action-item" @click="goToCategory({name: '面膜'})">
				<view class="action-icon new">✨</view>
				<text>新品上市</text>
			</view>
			<view class="action-item" @click="showToast('积分兑换开发中')">
				<view class="action-icon gift">🎁</view>
				<text>积分兑换</text>
			</view>
			<view class="action-item" @click="goToMember">
				<view class="action-icon vip">👑</view>
				<text>会员专享</text>
			</view>
		</view>

		<!-- 品牌墙 -->
		<view class="section brand-section">
			<view class="section-header">
				<view class="title-wrapper">
					<text class="section-title">合作品牌</text>
					<text class="section-desc">全球顶级医美品牌直供</text>
				</view>
			</view>
			<scroll-view class="brand-scroll" scroll-x>
				<view class="brand-list">
					<view class="brand-item" v-for="(brand, bIdx) in hotBrands" :key="bIdx" @click="searchByBrand(brand)">
						<view class="brand-logo-box">
							<text class="brand-name-mini">{{brand}}</text>
						</view>
					</view>
				</view>
			</scroll-view>
		</view>

		<!-- 严选专区 -->
		<view class="section">
			<view class="section-header">
				<view class="title-wrapper">
					<text class="section-title">正品严选</text>
					<text class="section-desc">每一支药品都可溯源</text>
				</view>
				<text class="section-more" @click="goToCategory({name: '全部'})">查看全部 </text>
			</view>
			<view class="product-list">
				<view class="loading-state" v-if="loading">
					<text>正在为您挑选精选商品...</text>
				</view>
				<view class="empty-state" v-else-if="products.length === 0">
					<text>暂无商品数据 (请检查 static/data/products.json)</text>
				</view>
				<view class="product-card" v-for="(item, index) in products" :key="index" @click="goToDetail(item)" v-else>
					<view class="product-image-wrapper">
						<image class="product-image" :src="item.image" mode="aspectFill" v-if="item.image" referrer-policy="no-referrer"></image>
						<view class="product-image" v-else></view>
						<view class="auth-badge">正品认证</view>
					</view>
					<view class="product-info">
						<text class="product-brand">{{item.brand}}</text>
						<text class="product-name">{{item.name}}</text>
						<view class="product-tag-row">
							<text class="tag" v-for="(tag, tIdx) in item.tags" :key="tIdx">{{tag}}</text>
						</view>
						<view class="product-footer">
							<view class="price-area">
								<view class="price-box">
									<text class="currency">￥</text>
									<text class="price">{{item.memberPrice || item.price}}</text>
								</view>
								<view class="vip-tag-wrapper">
									<view class="luxury-vip-tag" :style="{ background: memberLevel.bg, color: memberLevel.textColor, border: memberLevel.border }">
										{{memberLevel.name}}价
									</view>
								</view>
							</view>
							<view class="buy-btn">+</view>
						</view>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import { apiService, MEMBER_LEVELS } from '@/utils/api.js';

	export default {
		data() {
			return {
				banners: [
					{ title: '全球正品溯源', subtitle: '药监局合规备案 假一赔十', gradient: 'linear-gradient(135deg, #2C3E50 0%, #4CA1AF 100%)' },
					{ title: '医用修复专场', subtitle: '术后黄金修复期 专家严选', gradient: 'linear-gradient(135deg, #D4AF37 0%, #B8860B 100%)' }
				],
				categories: [],
				hotBrands: [],
				products: [],
				memberLevel: {},
				loading: true,
				loadError: false
			}
		},
		onLoad() {
			this.loadData();
		},
		onPullDownRefresh() {
			this.loadData().then(() => {
				uni.stopPullDownRefresh();
			});
		},
		methods: {
			async loadData() {
				console.log('首页加载数据...');
				this.loading = true;
				this.loadError = false;
				try {
					const levelKey = apiService.getCurrentMemberLevel();
					this.memberLevel = MEMBER_LEVELS[levelKey];
					
					// 加载分类
					const cats = await apiService.getCategories();
					const gradients = [
						'linear-gradient(135deg, #EBF5FB 0%, #AED6F1 100%)',
						'linear-gradient(135deg, #FEF5E7 0%, #FAD7A0 100%)',
						'linear-gradient(135deg, #EAFAF1 0%, #ABEBC6 100%)',
						'linear-gradient(135deg, #FBFCFC 0%, #D5DBDB 100%)',
						'linear-gradient(135deg, #F4ECF7 0%, #D7BDE2 100%)'
					];
					this.categories = cats.slice(0, 8).map((c, i) => ({
						...c,
						gradient: gradients[i % gradients.length]
					}));

					// 提取热门品牌
					if (cats.length > 4) {
						this.hotBrands = cats.slice(4, 14).map(c => c.name);
					}

					console.log('正在调用 getHomeProducts');
					const data = await apiService.getHomeProducts();
					console.log('首页商品数据量:', data ? data.length : 0);
					
					if (data && data.length > 0) {
						this.products = data.map(p => ({
							...p,

						memberPrice: apiService.calculateMemberPrice(p.purchasePrice)
						}));
					} else {
						this.loadError = true;
					}
				} catch (e) {
					console.error('加载商品失败', e);
					this.loadError = true;
				} finally {
					this.loading = false;
				}
			},
			searchByBrand(brand) {
				uni.navigateTo({
					url: `/pages/product/search?keyword=${brand}`
				});
			},
			goToDetail(item) {
				uni.navigateTo({
					url: '/pages/product/detail?id=' + (item.id || '')
				});
			},
			goToCategory(item) {
				if (item && item.name) {
					uni.setStorageSync('selectedCategory', item.name);
				}
				uni.switchTab({
					url: '/pages/services/services'
				});
			},
			goToSearch() {
				uni.navigateTo({
					url: '/pages/product/search'
				});
			}
		}
	}
</script>

<style lang="scss">
	.container {
		background-color: #F4F7F6;
		min-height: 100vh;
		padding-bottom: 40rpx;
		font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
	}

	.trust-header {
		display: flex;
		justify-content: space-around;
		padding: 15rpx 0;
		background-color: #fff;
		border-bottom: 1rpx solid #EBEEF5;
		
		.trust-item {
			display: flex;
			align-items: center;
			text {
				font-size: 22rpx;
				color: #7F8C8D;
				margin-left: 8rpx;
			}
		}
	}

	.search-bar {
		padding: 20rpx 30rpx;
		background-color: #fff;
		
		.search-input {
			height: 80rpx;
			background-color: #F2F4F4;
			border-radius: 12rpx;
			display: flex;
			align-items: center;
			padding: 0 30rpx;
			border: 1rpx solid #EBEEF5;
		}
		
		.placeholder {
			margin-left: 15rpx;
			font-size: 28rpx;
			color: #BDC3C7;
		}
	}

	.banner {
		height: 380rpx;
		background-color: #fff;
		padding: 20rpx 0;
		
		.banner-card {
			padding: 0 30rpx;
			height: 100%;
		}
		
		.banner-content {
			height: 100%;
			border-radius: 24rpx;
			padding: 50rpx;
			display: flex;
			flex-direction: column;
			justify-content: center;
			color: #fff;
			position: relative;
			overflow: hidden;
			box-shadow: 0 12rpx 30rpx rgba(0,0,0,0.15);
			
			&::after {
				content: '';
				position: absolute;
				top: -50%;
				right: -20%;
				width: 300rpx;
				height: 300rpx;
				background: rgba(255,255,255,0.1);
				border-radius: 50%;
			}
		}
		
		.banner-tag {
			position: absolute;
			top: 30rpx;
			right: 30rpx;
			background: rgba(255, 255, 255, 0.2);
			backdrop-filter: blur(10px);
			font-size: 20rpx;
			padding: 6rpx 20rpx;
			border-radius: 30rpx;
			border: 1rpx solid rgba(255,255,255,0.3);
		}
		
		.banner-title {
			font-size: 48rpx;
			font-weight: bold;
			margin-bottom: 15rpx;
			letter-spacing: 4rpx;
			text-shadow: 0 2rpx 10rpx rgba(0,0,0,0.2);
		}
		
		.banner-subtitle {
			font-size: 26rpx;
			opacity: 0.9;
			letter-spacing: 2rpx;
		}
	}

	.category-section {
		background-color: #fff;
		padding: 30rpx 0;
		margin-bottom: 20rpx;
		
		.category-grid {
			display: flex;
			flex-wrap: wrap;
		}
		
		.category-item {
			width: 25%;
			display: flex;
			flex-direction: column;
			align-items: center;
			margin-bottom: 30rpx;
			
			.category-icon-wrapper {
				width: 100rpx;
				height: 100rpx;
				margin-bottom: 15rpx;
				display: flex;
				align-items: center;
				justify-content: center;
			}
			
			.category-icon {
				width: 100%;
				height: 100%;
				border-radius: 30rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
				
				.cat-initial {
					color: #fff;
					font-size: 40rpx;
					font-weight: bold;
					text-shadow: 0 2rpx 4rpx rgba(0,0,0,0.1);
				}
			}
			
			.category-name {
				font-size: 24rpx;
				color: #2C3E50;
				font-weight: 500;
			}
		}
	}

	.quick-actions {
		display: flex;
		justify-content: space-around;
		padding: 20rpx 30rpx;
		background-color: #fff;
		margin-bottom: 20rpx;
		
		.action-item {
			display: flex;
			flex-direction: column;
			align-items: center;
			
			.action-icon {
				width: 80rpx;
				height: 80rpx;
				border-radius: 40rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				font-size: 40rpx;
				margin-bottom: 10rpx;
				background-color: #F8F9F9;
				
				&.hot { background-color: #FDEDEC; }
				&.new { background-color: #EBF5FB; }
				&.gift { background-color: #FEF9E7; }
				&.vip { background-color: #F4ECF7; }
			}
			
			text {
				font-size: 22rpx;
				color: #7F8C8D;
			}
		}
	}

	.brand-section {
		background-color: #fff;
		margin-top: 20rpx;
		padding-bottom: 30rpx;
		
		.brand-scroll {
			width: 100%;
			white-space: nowrap;
			padding: 0 30rpx;
			box-sizing: border-box;
		}
		
		.brand-list {
			display: inline-flex;
			padding: 10rpx 0;
		}
		
		.brand-item {
			margin-right: 20rpx;
			
			.brand-logo-box {
				width: 180rpx;
				height: 90rpx;
				background-color: #F8F9F9;
				border-radius: 12rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				border: 1rpx solid #EBEEF5;
				padding: 0 10rpx;
				
				.brand-name-mini {
					font-size: 22rpx;
					color: #2C3E50;
					font-weight: bold;
					text-align: center;
					white-space: normal;
					display: -webkit-box;
					-webkit-box-orient: vertical;
					-webkit-line-clamp: 2;
					overflow: hidden;
				}
			}
		}
	}

	.brand-section {
		background-color: #fff;
		padding-bottom: 30rpx;
		
		.brand-scroll {
			width: 100%;
			white-space: nowrap;
			
			.brand-list {
				display: inline-flex;
				padding: 0 30rpx;
				
				.brand-item {
					margin-right: 20rpx;
					
					.brand-logo-box {
						width: 160rpx;
						height: 80rpx;
						background-color: #F8F9F9;
						border-radius: 12rpx;
						display: flex;
						align-items: center;
						justify-content: center;
						border: 1rpx solid #F2F4F4;
						
						.brand-name-mini {
							font-size: 22rpx;
							color: #2C3E50;
							font-weight: 600;
							text-align: center;
							padding: 0 10rpx;
							overflow: hidden;
							text-overflow: ellipsis;
							white-space: nowrap;
						}
					}
				}
			}
		}
	}

	.section {
		background-color: #fff;
		padding: 40rpx 30rpx;
		
		.section-header {
			display: flex;
			justify-content: space-between;
			align-items: flex-end;
			margin-bottom: 40rpx;
		}
		
		.section-title {
			font-size: 36rpx;
			font-weight: bold;
			color: #2C3E50;
			display: block;
		}
		
		.section-desc {
			font-size: 22rpx;
			color: #7F8C8D;
			margin-top: 8rpx;
			display: block;
		}
		
		.section-more {
			font-size: 24rpx;
			color: #BDC3C7;
		}
	}

	.product-list {
		display: flex;
		flex-wrap: wrap;
		padding: 0 20rpx 20rpx 20rpx;
		justify-content: space-between;
		
		.loading-state, .empty-state {
			width: 100%;
			padding: 100rpx 0;
			text-align: center;
			color: #95A5A6;
			font-size: 28rpx;
		}
	}

	.product-card {
		width: calc((100% - 20rpx) / 2);
		background-color: #fff;
		border-radius: 16rpx; /* 更方正一点 */
		margin-bottom: 20rpx;
		overflow: hidden;
		box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.03); /* 极简阴影 */
		display: flex;
		flex-direction: column;
		border: 1rpx solid rgba(0,0,0,0.02); /* 微弱描边增加质感 */
		
		.product-image-wrapper {
			position: relative;
			width: 100%;
			height: 345rpx;
			background-color: #FAFAFA;
			flex-shrink: 0;
			
			.product-image {
				width: 100%;
				height: 100%;
			}
			
			.auth-badge {
				position: absolute;
				bottom: 0;
				left: 0;
				width: 100%;
				height: 48rpx;
				background: linear-gradient(to top, rgba(0,0,0,0.4), transparent);
				color: #fff;
				font-size: 18rpx;
				padding: 0 16rpx 10rpx 16rpx;
				display: flex;
				align-items: flex-end;
				letter-spacing: 2rpx;
				font-weight: 300;
				opacity: 0.9;
				top: auto; /* 覆盖旧样式 */
				border-radius: 0; /* 覆盖旧样式 */
				box-shadow: none; /* 覆盖旧样式 */
			}
		}
		
		.product-info {
			padding: 24rpx;
			flex: 1;
			display: flex;
			flex-direction: column;
			
			.product-brand {
				font-size: 20rpx;
				color: #999; /* 更高级的灰色 */
				font-weight: 500;
				margin-bottom: 12rpx;
				display: block;
				letter-spacing: 2rpx;
				text-transform: uppercase;
			}
			
			.product-name {
				font-size: 28rpx;
				color: #222; /* 深灰近黑 */
				font-weight: 500;
				height: 80rpx;
				line-height: 40rpx;
				display: -webkit-box;
				-webkit-box-orient: vertical;
				-webkit-line-clamp: 2;
				overflow: hidden;
				margin-bottom: 24rpx;
				font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, sans-serif;
			}
			
			.product-tag-row {
				display: flex;
				flex-wrap: wrap;
				height: 32rpx;
				overflow: hidden;
				margin-bottom: 28rpx;
				
				.tag {
					font-size: 16rpx;
					color: #666;
					border: 1rpx solid #E0E0E0; /* 线性标签更显高级 */
					background-color: transparent;
					padding: 0 10rpx;
					height: 28rpx;
					line-height: 26rpx;
					border-radius: 4rpx;
					margin-right: 8rpx;
				}
			}
			
			.product-footer {
				margin-top: auto;
				display: flex;
				flex-direction: row;
				justify-content: space-between;
				align-items: flex-end;
				
				.price-area {
					display: flex;
					flex-direction: column;
					flex: 1;
					
					.price-box {
						display: flex;
						align-items: baseline;
						margin-bottom: 8rpx;
						
						.currency {
							font-size: 24rpx;
							color: #222; /* 价格回归黑色，强调专业 */
							font-weight: normal;
							margin-right: 2rpx;
						}
						.price {
							font-size: 38rpx;
							color: #222;
							font-weight: 500;
							margin-right: 4rpx;
							font-family: 'DIN Alternate', 'Helvetica Neue', sans-serif;
							line-height: 1;
							letter-spacing: -1rpx;
						}
					}
					
					.vip-tag-wrapper {
						display: flex;
						
						.luxury-vip-tag {
							font-size: 18rpx;
							padding: 0 8rpx;
							height: 30rpx;
							line-height: 30rpx;
							border-radius: 4rpx;
							font-weight: 500;
							display: inline-flex;
							align-items: center;
							/* 覆盖内联样式，使用黑金配色 */
							background: #222 !important; 
							color: #E0CFA6 !important;
							border: none !important;
						}
					}
				}
				
				.buy-btn {
					background: #222; /* 纯黑按钮 */
					color: #fff;
					width: 56rpx;
					height: 56rpx;
					border-radius: 50%;
					display: flex;
					align-items: center;
					justify-content: center;
					font-size: 36rpx;
					font-weight: 200;
					box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.15);
					margin-bottom: 2rpx;
					flex-shrink: 0;
					transition: all 0.2s;
				}
				.buy-btn:active {
					transform: scale(0.95);
					background: #000;
				}
			}
		}
	}
</style>
