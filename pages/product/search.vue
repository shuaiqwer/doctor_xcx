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
			<view class="product-list" v-else>
				<view class="product-card" v-for="(item, index) in results" :key="index" @click="goToDetail(item.id)">
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
	
	.product-list {
		display: flex;
		flex-wrap: wrap;
		padding: 20rpx;
		justify-content: space-between;
	}

	.product-card {
		width: calc((100% - 20rpx) / 2);
		background-color: #fff;
		border-radius: 16rpx;
		margin-bottom: 20rpx;
		overflow: hidden;
		box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.03);
		display: flex;
		flex-direction: column;
		border: 1rpx solid rgba(0,0,0,0.02);
		
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
			}
		}
		
		.product-info {
			padding: 24rpx;
			flex: 1;
			display: flex;
			flex-direction: column;
			
			.product-brand {
				font-size: 20rpx;
				color: #999;
				font-weight: 500;
				margin-bottom: 12rpx;
				display: block;
				letter-spacing: 2rpx;
				text-transform: uppercase;
			}
			
			.product-name {
				font-size: 28rpx;
				color: #222;
				font-weight: 500;
				height: 80rpx;
				line-height: 40rpx;
				display: -webkit-box;
				-webkit-box-orient: vertical;
				-webkit-line-clamp: 2;
				overflow: hidden;
				margin-bottom: 24rpx;
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
					border: 1rpx solid #E0E0E0;
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
							color: #222;
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
							background: #222 !important; 
							color: #E0CFA6 !important;
							border: none !important;
						}
					}
				}
				
				.buy-btn {
					background: #222;
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
				}
			}
		}
	}
}
</style>
