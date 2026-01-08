<template>
	<view class="container">
		<!-- 搜索头部 -->
		<view class="search-header">
			<view class="status-bar"></view>
			<view class="search-input-row">
				<view class="back-btn" @click="goBack">
					<text class="back-arrow"></text>
				</view>
				<view class="search-box">
					<icon type="search" size="16" color="#999" />
					<input 
						type="text" 
						v-model="keyword" 
						placeholder="搜索正品医美药品" 
						confirm-type="search"
						@confirm="handleSearch"
						focus
					/>
					<icon type="clear" size="16" color="#ccc" v-if="keyword" @click="keyword = ''" />
				</view>
				<view class="search-btn" @click="handleSearch">搜索</view>
			</view>
		</view>

		<!-- 搜索历史/热门搜索 (初始状态) -->
		<view class="search-suggest" v-if="!isSearching && results.length === 0">
			<view class="section">
				<view class="section-title">
					<text>热门搜索</text>
				</view>
				<view class="tag-list">
					<view class="tag" v-for="(item, index) in hotKeywords" :key="index" @click="quickSearch(item)">
						{{item}}
					</view>
				</view>
			</view>
		</view>

		<!-- 搜索结果列表 -->
		<scroll-view class="result-list" scroll-y v-else>
			<view class="loading-box" v-if="loading">
				<text>正在搜索中...</text>
			</view>
			<view class="empty-box" v-else-if="results.length === 0">
				<image src="/static/empty-search.png" mode="aspectFit" class="empty-img"></image>
				<text>未找到相关商品</text>
			</view>
			<view class="product-grid" v-else>
				<view class="product-card" v-for="(item, index) in results" :key="index" @click="goToDetail(item.id)">
					<image class="product-image" :src="item.image" mode="aspectFill" referrer-policy="no-referrer"></image>
					<view class="product-info">
						<text class="product-name">{{item.name}}</text>
						<view class="product-footer">
							<view class="price-box">
								<text class="price">￥{{item.memberPrice || item.price}}</text>
								<view class="luxury-vip-tag" :style="{ background: memberLevel.bg, color: memberLevel.textColor, border: memberLevel.border }">
									{{memberLevel.name}}
								</view>
							</view>
							<text class="sales">销量 {{item.sales || 0}}</text>
						</view>
					</view>
				</view>
			</view>
		</scroll-view>
	</view>
</template>

<script>
	import { apiService, MEMBER_LEVELS } from '@/utils/api.js';

	export default {
		data() {
			return {
				keyword: '',
				isSearching: false,
				loading: false,
				results: [],
				hotKeywords: ['水光', '面膜', '润百颜', '修丽可', '胶原蛋白', '修复'],
				allProducts: [],
				memberLevel: {}
			}
		},
		async onLoad(options) {
			const levelKey = apiService.getCurrentMemberLevel();
			this.memberLevel = MEMBER_LEVELS[levelKey];

			if (options.keyword) {
				this.keyword = options.keyword;
				this.handleSearch();
			}
		},
		methods: {
			goBack() {
				uni.navigateBack();
			},
			quickSearch(kw) {
				this.keyword = kw;
				this.handleSearch();
			},
			async handleSearch() {
				if (!this.keyword.trim()) return;
				
				this.isSearching = true;
				this.loading = true;
				
				try {
					const res = await apiService.getProducts({
						page: 1,
						pageSize: 100, // 搜索时多加载一些
						keyword: this.keyword
					});
					
					const list = res.list || [];
					this.results = list.map(p => ({
						...p,
					memberPrice: apiService.calculateMemberPrice(p.purchasePrice)
					}));
				} catch (e) {
					console.error('搜索失败', e);
					this.results = [];
				} finally {
					this.loading = false;
				}
			},
			goToDetail(id) {
				uni.navigateTo({
					url: `/pages/product/detail?id=${id}`
				});
			}
		}
	}
</script>

<script setup>
// 如果需要使用 uni-app 的一些组合式 API
</script>

<style lang="scss">
.container {
	height: 100vh;
	display: flex;
	flex-direction: column;
	background-color: #F8F9FA;
}

.search-header {
	background-color: #fff;
	padding-bottom: 20rpx;
	
	.status-bar {
		height: var(--status-bar-height);
	}
	
	.search-input-row {
		display: flex;
		align-items: center;
		padding: 10rpx 30rpx;
		
		.back-btn {
			padding-right: 20rpx;
			display: flex;
			align-items: center;
			
			.back-arrow {
				width: 20rpx;
				height: 20rpx;
				border-left: 4rpx solid #333;
				border-bottom: 4rpx solid #333;
				transform: rotate(45deg);
				margin-left: 10rpx;
			}
		}
		
		.search-box {
			flex: 1;
			height: 72rpx;
			background: #F1F2F6;
			border-radius: 36rpx;
			display: flex;
			align-items: center;
			padding: 0 24rpx;
			
			input {
				flex: 1;
				margin-left: 12rpx;
				font-size: 28rpx;
			}
		}
		
		.search-btn {
			padding-left: 24rpx;
			font-size: 28rpx;
			color: #D4AF37;
			font-weight: bold;
		}
	}
}

.search-suggest {
	padding: 40rpx 30rpx;
	
	.section {
		margin-bottom: 40rpx;
		
		.section-title {
			font-size: 30rpx;
			font-weight: bold;
			color: #2C3E50;
			margin-bottom: 24rpx;
		}
		
		.tag-list {
			display: flex;
			flex-wrap: wrap;
			
			.tag {
				padding: 12rpx 28rpx;
				background: #fff;
				border-radius: 30rpx;
				font-size: 24rpx;
				color: #666;
				margin-right: 20rpx;
				margin-bottom: 20rpx;
				border: 1rpx solid #EEE;
			}
		}
	}
}

.result-list {
	flex: 1;
	padding: 20rpx;
	
	.loading-box, .empty-box {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding-top: 200rpx;
		color: #999;
		font-size: 28rpx;
		
		.empty-img {
			width: 200rpx;
			height: 200rpx;
			margin-bottom: 20rpx;
			opacity: 0.5;
		}
	}
	
	.product-grid {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		
		.product-card {
			width: 48.5%;
			background: #fff;
			border-radius: 16rpx;
			margin-bottom: 20rpx;
			overflow: hidden;
			box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.03);
			
			.product-image {
				width: 100%;
				height: 340rpx;
				background-color: #F8F9F9;
			}
			
			.product-info {
				padding: 20rpx;
				
				.product-name {
					font-size: 26rpx;
					color: #2C3E50;
					font-weight: 500;
					height: 72rpx;
					line-height: 36rpx;
					display: -webkit-box;
					-webkit-box-orient: vertical;
					-webkit-line-clamp: 2;
					overflow: hidden;
					margin-bottom: 15rpx;
				}
				
				.product-footer {
					display: flex;
					flex-direction: column;
					
					.price-box {
						display: flex;
						align-items: center;
						margin-bottom: 10rpx;
						
						.price {
							font-size: 32rpx;
							color: #D4AF37;
							font-weight: bold;
							margin-right: 10rpx;
						}
						
						.luxury-vip-tag {
							font-size: 18rpx;
							padding: 2rpx 8rpx;
							border-radius: 4rpx;
						}
					}
					
					.sales {
						font-size: 20rpx;
						color: #BDC3C7;
					}
				}
			}
		}
	}
}
</style>
