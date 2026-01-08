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
						<view class="drug-grid" v-else>
							<view class="drug-item" v-for="(product, pIdx) in currentProducts" :key="pIdx" @click="goToDetail(product.id)">
								<view class="drug-image-box">
									<image :src="product.image" mode="aspectFill" class="drug-image" referrer-policy="no-referrer"></image>
								</view>
								<text class="drug-name">{{product.name}}</text>
								<view class="price-row">
									<text class="drug-price">¥{{product.memberPrice || product.price}}</text>
									<view class="luxury-vip-tag" :style="{ background: memberLevel.bg, color: memberLevel.textColor, border: memberLevel.border }">
										VIP
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

	.drug-grid {
		display: flex;
		flex-wrap: wrap;
		
		.drug-item {
			width: 50%;
			display: flex;
			flex-direction: column;
			padding: 15rpx;
			box-sizing: border-box;
			margin-bottom: 20rpx;
			cursor: pointer;
			transition: transform 0.2s;
			
			&:active {
				transform: scale(0.98);
			}
			
			.drug-image-box {
				width: 100%;
				height: 240rpx;
				background-color: #F8F9F9;
				border-radius: 16rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				margin-bottom: 15rpx;
				border: 1rpx solid #EBEEF5;
				overflow: hidden;
				
				.drug-image {
					width: 100%;
					height: 100%;
					object-fit: cover;
				}
			}
			
			.drug-name {
				font-size: 24rpx;
				color: #2C3E50;
				font-weight: 500;
				display: -webkit-box;
				-webkit-box-orient: vertical;
				-webkit-line-clamp: 2;
				overflow: hidden;
				height: 64rpx;
				line-height: 32rpx;
				margin-bottom: 10rpx;
			}

			.price-row {
				display: flex;
				align-items: center;
				justify-content: space-between;
				
				.drug-price {
					font-size: 28rpx;
					color: #D4AF37;
					font-weight: bold;
				}

				.luxury-vip-tag {
					font-size: 16rpx;
					padding: 4rpx 10rpx;
					border-radius: 4rpx;
					font-weight: bold;
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
