<template>
	<view class="container">
		<!-- 状态切换 -->
		<view class="tabs">
			<view 
				v-for="(tab, index) in tabs" 
				:key="index" 
				class="tab-item" 
				:class="{ active: currentIndex === index }"
				@click="currentIndex = index"
			>
				{{tab}}
			</view>
		</view>

		<!-- 订单列表 -->
		<scroll-view class="order-list" scroll-y>
			<view class="order-card" v-for="(order, index) in filteredOrders" :key="index">
				<view class="card-header">
					<text class="order-no">订单号：ORD20260103{{index}}</text>
					<text class="status">{{order.statusText}}</text>
				</view>
				<view class="card-body">
					<view class="product-img"></view>
					<view class="product-info">
						<text class="name">{{order.productName}}</text>
						<view class="price-row">
							<text class="price">￥{{order.price}}</text>
							<text class="num">x{{order.num}}</text>
						</view>
					</view>
				</view>
				<view class="card-footer">
					<view class="total-info">
						共{{order.num}}件商品 实付：<text class="total-price">￥{{order.totalPrice}}</text>
					</view>
					<view class="action-btns">
						<view class="btn outline" v-if="order.status === 0" @click="showToast('订单已取消')">取消订单</view>
						<view class="btn solid" v-if="order.status === 0" @click="goToPay(order)">去支付</view>
						<view class="btn outline" v-if="order.status === 2" @click="showToast('物流信息查询中')">查看物流</view>
						<view class="btn solid" v-if="order.status === 2" @click="showToast('已确认收货')">确认收货</view>
						<view class="btn outline" v-if="order.status === 3" @click="goToDetail">再次购买</view>
					</view>
				</view>
			</view>
			
			<view class="empty-state" v-if="filteredOrders.length === 0">
				<icon type="info" size="40" color="#BDC3C7" />
				<text>暂无相关订单</text>
			</view>
		</scroll-view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				currentIndex: 0,
				tabs: ['全部', '待付款', '待发货', '待收货', '已完成'],
				orders: [
					{ 
						status: 2, 
						statusText: '待收货', 
						productName: '【正品】菲洛嘉135HA 能量青春动能素 3ml*5支/盒', 
						price: '1280.00', 
						num: 1, 
						totalPrice: '1280.00' 
					},
					{ 
						status: 3, 
						statusText: '已完成', 
						productName: '【医用】可复美 类人胶原蛋白敷料 5片/盒', 
						price: '128.00', 
						num: 2, 
						totalPrice: '256.00' 
					}
				]
			}
		},
		computed: {
			filteredOrders() {
				if (this.currentIndex === 0) return this.orders;
				// 简单模拟过滤逻辑
				const statusMap = [null, 0, 1, 2, 3];
				return this.orders.filter(o => o.status === statusMap[this.currentIndex]);
			}
		},
		methods: {
			showToast(msg) {
				uni.showToast({
					title: msg,
					icon: 'none'
				});
			},
			goToPay(order) {
				uni.navigateTo({
					url: '/pages/order/confirm'
				});
			},
			goToDetail() {
				uni.navigateTo({
					url: '/pages/product/detail'
				});
			}
		}
	}
</script>

<style lang="scss">
	.container {
		background-color: #F4F7F6;
		min-height: 100vh;
		display: flex;
		flex-direction: column;
	}

	.tabs {
		display: flex;
		background-color: #fff;
		height: 90rpx;
		border-bottom: 1rpx solid #EBEEF5;
		
		.tab-item {
			flex: 1;
			display: flex;
			align-items: center;
			justify-content: center;
			font-size: 28rpx;
			color: #7F8C8D;
			position: relative;
			
			&.active {
				color: #2C3E50;
				font-weight: bold;
				&::after {
					content: '';
					position: absolute;
					bottom: 0;
					left: 50%;
					transform: translateX(-50%);
					width: 40rpx;
					height: 4rpx;
					background-color: #D4AF37;
				}
			}
		}
	}

	.order-list {
		flex: 1;
		padding: 20rpx;
	}

	.order-card {
		background-color: #fff;
		border-radius: 20rpx;
		padding: 30rpx;
		margin-bottom: 20rpx;
		
		.card-header {
			display: flex;
			justify-content: space-between;
			margin-bottom: 30rpx;
			.order-no { font-size: 24rpx; color: #BDC3C7; }
			.status { font-size: 26rpx; color: #D4AF37; font-weight: bold; }
		}
		
		.card-body {
			display: flex;
			margin-bottom: 30rpx;
			.product-img {
				width: 140rpx;
				height: 140rpx;
				background-color: #F8F9F9;
				border-radius: 12rpx;
				margin-right: 20rpx;
			}
			.product-info {
				flex: 1;
				display: flex;
				flex-direction: column;
				justify-content: space-between;
				.name { font-size: 28rpx; color: #2C3E50; line-height: 36rpx; }
				.price-row {
					display: flex;
					justify-content: space-between;
					.price { font-size: 28rpx; color: #2C3E50; font-weight: bold; }
					.num { font-size: 24rpx; color: #BDC3C7; }
				}
			}
		}
		
		.card-footer {
			border-top: 1rpx solid #F2F4F4;
			padding-top: 30rpx;
			.total-info {
				text-align: right;
				font-size: 24rpx;
				color: #7F8C8D;
				margin-bottom: 20rpx;
				.total-price { font-size: 32rpx; color: #2C3E50; font-weight: bold; }
			}
			.action-btns {
				display: flex;
				justify-content: flex-end;
				.btn {
					padding: 12rpx 30rpx;
					border-radius: 30rpx;
					font-size: 24rpx;
					margin-left: 20rpx;
					
					&.outline { border: 1rpx solid #EBEEF5; color: #7F8C8D; }
					&.solid { background-color: #2C3E50; color: #fff; }
				}
			}
		}
	}

	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding-top: 200rpx;
		text { font-size: 28rpx; color: #BDC3C7; margin-top: 20rpx; }
	}
</style>
