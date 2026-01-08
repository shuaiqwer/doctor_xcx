<template>
	<view class="container">
		<view class="search-header">
			<view class="search-box" @click="goToSearch()">
				<icon type="search" size="14" color="#BDC3C7" />
				<text>搜索分类下的药品</text>
			</view>
		</view>
		
		<view class="category-wrapper">
			<!-- 左侧分类导航 -->
			<scroll-view class="left-aside" scroll-y>
				<view 
					v-for="(item, index) in categoryList" 
					:key="index" 
					class="nav-item" 
					:class="{ active: index === currentIndex }"
					@click="selectCategory(index)"
				>
					<text>{{item.name}}</text>
				</view>
			</scroll-view>

			<!-- 右侧药品列表 -->
			<scroll-view class="right-main" scroll-y v-if="categoryList.length > 0">
				<view class="category-content">
					<view class="banner-mini" :style="{ background: categoryList[currentIndex].gradient }">
						<text class="banner-title">{{categoryList[currentIndex].name}}专区</text>
						<text class="banner-tips">正品保障 · 专家严选</text>
					</view>
					
					<view class="drug-section">
						<view class="empty-list" v-if="!loading && currentProducts.length === 0">
							<view class="empty-icon-box">📦</view>
							<text class="empty-text">{{ errorMsg || '该分类下暂无商品' }}</text>
							<button class="retry-btn" @click="retryInit">重新加载</button>
						</view>
						<view class="product-list" v-else>
							<view class="product-card" v-for="(item, index) in currentProducts" :key="index" @click="goToDetail(item.id)">
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
						
						<!-- 手动分页控制栏 -->
						<view class="pagination-bar" v-if="currentProducts.length > 0">
							<button class="page-btn" :disabled="page === 1" @click="prevPage">上一页</button>
							<view class="page-info">
								<text class="current">{{page}}</text>
								<text class="split">/</text>
								<text class="total">{{totalPages || 1}}</text>
							</view>
							<button class="page-btn" :disabled="page >= totalPages" @click="nextPage">下一页</button>
						</view>

						<view class="loading-status" v-if="loading">
							<text>正在加载数据...</text>
						</view>
					</view>
				</view>
			</scroll-view>
		</view>
	</view>
</template>

<script>
	import { apiService, MEMBER_LEVELS } from '@/utils/api.js';

	export default {
		data() {
			return {
				currentIndex: 0,
				categoryList: [],
				currentProducts: [], // 当前页的商品列表
				memberLevel: {},
				page: 1,
				pageSize: 10,
				total: 0,
				totalPages: 1,
				loading: false,
				errorMsg: ''
			}
		},
		onLoad() {
			console.log('分类页面加载');
			this.initData();
		},
		onShow() {
			const selected = uni.getStorageSync('selectedCategory');
			if (selected && this.categoryList.length > 0) {
				const index = this.categoryList.findIndex(c => c.name === selected);
				if (index > -1 && index !== this.currentIndex) {
					this.currentIndex = index;
					this.page = 1;
					this.loadProducts();
				}
				uni.removeStorageSync('selectedCategory');
			}
		},
		onPullDownRefresh() {
			this.page = 1;
			this.initData().then(() => {
				uni.stopPullDownRefresh();
			});
		},
		methods: {
			async initData() {
				console.log('[services] 开始初始化分类数据');
				try {
					const levelKey = apiService.getCurrentMemberLevel();
					this.memberLevel = MEMBER_LEVELS[levelKey];

					// 获取分类列表
					console.log('[services] 正在请求分类列表...');
					const categories = await apiService.getCategories();
					console.log('[services] 获取到分类数量:', categories ? categories.length : 0);
					
					// 为每个分类添加渐变背景
					const gradients = [
						'linear-gradient(135deg, #EBF5FB 0%, #AED6F1 100%)',
						'linear-gradient(135deg, #FEF5E7 0%, #FAD7A0 100%)',
						'linear-gradient(135deg, #EAFAF1 0%, #ABEBC6 100%)',
						'linear-gradient(135deg, #FBFCFC 0%, #D5DBDB 100%)',
						'linear-gradient(135deg, #F4ECF7 0%, #D7BDE2 100%)'
					];
					this.categoryList = categories.map((item, index) => ({
						...item,
						gradient: gradients[index % gradients.length]
					}));

					// 加载第一个分类的商品
					if (this.categoryList.length > 0) {
						console.log('[services] 初始加载第一个分类商品:', this.categoryList[0].name);
						this.loadProducts();
					} else {
						console.warn('[services] 分类列表为空！');
					}
				} catch (e) {
					console.error('[services] 初始化过程报错:', e);
				}
			},
			async loadProducts() {
				if (this.loading) return;
				
				this.loading = true;
				this.errorMsg = '';
				const currentCat = this.categoryList[this.currentIndex];
				console.log('[services] 准备请求商品, 分类:', currentCat ? currentCat.name : '未知');
				
				try {
					const categoryName = currentCat ? currentCat.name : '全部';
					// 调用 API 获取分页数据
					const res = await apiService.getProducts({
						page: this.page,
						pageSize: this.pageSize,
						category: categoryName
					});
					
					console.log('[services] getProducts 响应结果:', res);
					
					if (res.error) {
						this.errorMsg = '数据加载失败: ' + res.error;
					}

					// 处理返回的数据格式
					const list = res.list || [];
					this.total = res.total || list.length;
					this.totalPages = Math.ceil(this.total / this.pageSize);
					
					console.log('[services] 解析后的商品数量:', list.length, '总数:', this.total);

					this.currentProducts = list.map(p => ({
						...p,
						memberPrice: apiService.calculateMemberPrice(p.purchasePrice)
					}));
				} catch (e) {
					console.error('[services] 加载商品过程报错:', e);
				} finally {
					this.loading = false;
				}
			},
			selectCategory(index) {
				if (this.currentIndex === index) return;
				this.currentIndex = index;
				this.page = 1; // 切换分类重置页码
				this.loadProducts();
			},
			retryInit() {
				if (this.categoryList.length === 0) {
					this.initData();
				} else {
					this.loadProducts();
				}
			},
			prevPage() {
				if (this.page > 1) {
					this.page--;
					this.loadProducts();
				}
			},
			nextPage() {
				if (this.page < this.totalPages) {
					this.page++;
					this.loadProducts();
				}
			},
			goToSearch() {
				uni.navigateTo({
					url: '/pages/product/search'
				});
			},
			goToDetail(id) {
				uni.navigateTo({
					url: `/pages/product/detail?id=${id}`
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
		height: 100vh;
		display: flex;
		flex-direction: column;
		background-color: #fff;
	}
	
	.search-header {
		padding: 20rpx 30rpx;
		background-color: #fff;
		border-bottom: 1rpx solid #EBEEF5;
		
		.search-box {
			height: 64rpx;
			background-color: #F2F4F4;
			border-radius: 32rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			
			text {
				font-size: 24rpx;
				color: #BDC3C7;
				margin-left: 10rpx;
			}
		}
	}

	.category-wrapper {
		flex: 1;
		display: flex;
		overflow: hidden;
	}
	
	.left-aside {
		width: 180rpx;
		background-color: #F8F9F9;
		height: 100%;
		
		.nav-item {
			height: 110rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			font-size: 26rpx;
			color: #7F8C8D;
			position: relative;
			transition: all 0.3s;
			
			&.active {
				background-color: #fff;
				color: #2C3E50;
				font-weight: bold;
				
				&::before {
					content: '';
					position: absolute;
					left: 0;
					width: 6rpx;
					height: 36rpx;
					background-color: #D4AF37;
					border-radius: 0 4rpx 4rpx 0;
				}
			}
		}
	}

	.right-main {
		flex: 1;
		background-color: #fff;
		height: 100%;
		
		.category-content {
			padding: 20rpx;
		}
		
		.banner-mini {
			height: 160rpx;
			border-radius: 16rpx;
			padding: 30rpx;
			display: flex;
			flex-direction: column;
			justify-content: center;
			margin-bottom: 30rpx;
			box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
			
			.banner-title {
				font-size: 32rpx;
				font-weight: bold;
				color: #2C3E50;
				margin-bottom: 8rpx;
			}
			
			.banner-tips {
				font-size: 20rpx;
				color: #7F8C8D;
			}
		}
	}

	.product-list {
		display: flex;
		flex-wrap: wrap;
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
		width: calc((100% - 15rpx) / 2); /* 稍微调整间距以适应侧边栏后的宽度 */
		background-color: #fff;
		border-radius: 12rpx;
		margin-bottom: 20rpx;
		overflow: hidden;
		box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.03);
		display: flex;
		flex-direction: column;
		border: 1rpx solid rgba(0,0,0,0.02);
		
		.product-image-wrapper {
			position: relative;
			width: 100%;
			height: 260rpx; /* 侧边栏模式下图片由于宽度限制，高度也相应调小 */
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
				height: 40rpx;
				background: linear-gradient(to top, rgba(0,0,0,0.4), transparent);
				color: #fff;
				font-size: 16rpx;
				padding: 0 12rpx 6rpx 12rpx;
				display: flex;
				align-items: flex-end;
				letter-spacing: 1rpx;
				font-weight: 300;
				opacity: 0.9;
			}
		}
		
		.product-info {
			padding: 16rpx;
			flex: 1;
			display: flex;
			flex-direction: column;
			
			.product-brand {
				font-size: 18rpx;
				color: #999;
				font-weight: 500;
				margin-bottom: 8rpx;
				display: block;
				letter-spacing: 1rpx;
				text-transform: uppercase;
			}
			
			.product-name {
				font-size: 24rpx;
				color: #222;
				font-weight: 500;
				height: 68rpx;
				line-height: 34rpx;
				display: -webkit-box;
				-webkit-box-orient: vertical;
				-webkit-line-clamp: 2;
				overflow: hidden;
				margin-bottom: 16rpx;
			}
			
			.product-tag-row {
				display: flex;
				flex-wrap: wrap;
				height: 28rpx;
				overflow: hidden;
				margin-bottom: 20rpx;
				
				.tag {
					font-size: 14rpx;
					color: #666;
					border: 1rpx solid #E0E0E0;
					background-color: transparent;
					padding: 0 8rpx;
					height: 24rpx;
					line-height: 22rpx;
					border-radius: 4rpx;
					margin-right: 6rpx;
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
						margin-bottom: 4rpx;
						
						.currency {
							font-size: 20rpx;
							color: #222;
							font-weight: normal;
							margin-right: 2rpx;
						}
						.price {
							font-size: 32rpx;
							color: #222;
							font-weight: 500;
							margin-right: 4rpx;
							font-family: 'DIN Alternate', 'Helvetica Neue', sans-serif;
							line-height: 1;
						}
					}
					
					.vip-tag-wrapper {
						display: flex;
						
						.luxury-vip-tag {
							font-size: 16rpx;
							padding: 0 6rpx;
							height: 26rpx;
							line-height: 26rpx;
							border-radius: 4rpx;
							font-weight: 500;
							display: inline-flex;
							align-items: center;
							background: #222 !important; 
							color: #E0CFA6 !important;
							border: none !important;
						}
					}
				}
				
				.buy-btn {
					background: #222;
					color: #fff;
					width: 48rpx;
					height: 48rpx;
					border-radius: 50%;
					display: flex;
					align-items: center;
					justify-content: center;
					font-size: 32rpx;
					font-weight: 200;
					flex-shrink: 0;
				}
			}
		}
	}

	.empty-list {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 100rpx 0;
		width: 100%;

		.empty-img {
			width: 200rpx;
			height: 200rpx;
			margin-bottom: 30rpx;
			opacity: 0.5;
		}

		.empty-text {
			font-size: 28rpx;
			color: #95A5A6;
			margin-bottom: 40rpx;
		}

		.retry-btn {
			width: 240rpx;
			height: 70rpx;
			line-height: 70rpx;
			background-color: #D4AF37;
			color: #fff;
			font-size: 26rpx;
			border-radius: 35rpx;
		}
	}

	.pagination-bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 40rpx 20rpx;
		width: 100%;

		.page-btn {
			width: 160rpx;
			height: 64rpx;
			line-height: 64rpx;
			font-size: 24rpx;
			background-color: #fff;
			border: 1rpx solid #D4AF37;
			color: #D4AF37;
			border-radius: 32rpx;
			margin: 0;
			
			&[disabled] {
				border-color: #EBEEF5;
				color: #BDC3C7;
				background-color: #F8F9F9;
			}
		}

		.page-info {
			display: flex;
			align-items: center;
			font-size: 28rpx;
			color: #2C3E50;

			.current {
				color: #D4AF37;
				font-weight: bold;
			}
			.split {
				margin: 0 10rpx;
				color: #BDC3C7;
			}
			.total {
				color: #7F8C8D;
			}
		}
	}

	.loading-status {
		padding: 30rpx;
		text-align: center;
		font-size: 24rpx;
		color: #999;
		width: 100%;
	}
</style>
