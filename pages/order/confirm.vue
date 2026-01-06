<template>
	<view class="container">
		<!-- 收货地址 -->
		<view class="address-section" @click="selectAddress">
			<view class="address-content" v-if="address">
				<view class="user-info">
					<text class="name">{{address.name}}</text>
					<text class="phone">{{address.phone}}</text>
				</view>
				<view class="address-detail">{{address.province}}{{address.city}}{{address.district}}{{address.detail}}</view>
			</view>
			<view class="no-address" v-else>
				<icon type="download" size="20" color="#2C3E50" />
				<text>请选择收货地址</text>
			</view>
			<text class="arrow">></text>
		</view>

		<!-- 商品清单 -->
		<view class="product-section">
			<view class="section-title">商品清单</view>
			<view class="product-item">
				<view class="product-img"></view>
				<view class="product-info">
					<text class="name">【正品】菲洛嘉135HA 能量青春动能素 3ml*5支/盒</text>
					<view class="price-row">
						<text class="price">￥1280.00</text>
						<text class="num">x1</text>
					</view>
				</view>
			</view>
		</view>

		<!-- 费用明细 -->
		<view class="fee-section">
			<view class="fee-item">
				<text>商品总额</text>
				<text>￥1280.00</text>
			</view>
			<view class="fee-item">
				<text>运费</text>
				<text>￥0.00</text>
			</view>
			<view class="fee-item total">
				<text>实付款</text>
				<text class="total-price">￥1280.00</text>
			</view>
		</view>

		<!-- 支付方式 -->
		<view class="pay-section">
			<view class="section-title">支付方式</view>
			<view class="pay-item">
				<view class="pay-left">
					<icon type="success" size="20" color="#09BB07" />
					<text>微信支付</text>
				</view>
				<radio checked color="#2C3E50" />
			</view>
		</view>

		<!-- 底部提交栏 -->
		<view class="footer-bar">
			<view class="total-info">
				<text>合计：</text>
				<text class="price">￥1280.00</text>
			</view>
			<view class="submit-btn" @click="handlePay">立即支付</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				address: {
					name: '张医生',
					phone: '138****8888',
					province: '上海市',
					city: '上海市',
					district: '静安区',
					detail: '南京西路1234号 悦容诊所'
				}
			}
		},
		methods: {
			selectAddress() {
				uni.navigateTo({
					url: '/pages/address/list'
				});
			},
			handlePay() {
				uni.showLoading({ title: '支付中...' });
				setTimeout(() => {
					uni.hideLoading();
					uni.showToast({
						title: '支付成功',
						icon: 'success'
					});
					setTimeout(() => {
						uni.redirectTo({
							url: '/pages/order/list'
						});
					}, 1500);
				}, 2000);
			}
		}
	}
</script>

<style lang="scss">
	.container {
		background-color: #F4F7F6;
		min-height: 100vh;
		padding: 20rpx 0 120rpx;
	}

	.address-section {
		background-color: #fff;
		padding: 40rpx 30rpx;
		margin-bottom: 20rpx;
		display: flex;
		align-items: center;
		position: relative;
		
		.address-content {
			flex: 1;
			.user-info {
				margin-bottom: 10rpx;
				.name { font-size: 32rpx; font-weight: bold; color: #2C3E50; margin-right: 20rpx; }
				.phone { font-size: 28rpx; color: #7F8C8D; }
			}
			.address-detail { font-size: 26rpx; color: #2C3E50; line-height: 36rpx; }
		}
		
		.no-address {
			flex: 1;
			display: flex;
			align-items: center;
			text { font-size: 30rpx; color: #2C3E50; margin-left: 20rpx; }
		}
		
		.arrow { font-size: 30rpx; color: #BDC3C7; }
	}

	.product-section, .fee-section, .pay-section {
		background-color: #fff;
		padding: 30rpx;
		margin-bottom: 20rpx;
		
		.section-title {
			font-size: 28rpx;
			font-weight: bold;
			color: #2C3E50;
			margin-bottom: 30rpx;
		}
	}

	.product-item {
		display: flex;
		.product-img {
			width: 160rpx;
			height: 160rpx;
			background-color: #F8F9F9;
			border-radius: 12rpx;
			margin-right: 20rpx;
		}
		.product-info {
			flex: 1;
			display: flex;
			flex-direction: column;
			justify-content: space-between;
			.name { font-size: 28rpx; color: #2C3E50; line-height: 40rpx; font-weight: 500; }
			.price-row {
				display: flex;
				justify-content: space-between;
				.price { font-size: 30rpx; color: #E74C3C; font-weight: bold; }
				.num { font-size: 26rpx; color: #BDC3C7; }
			}
		}
	}

	.fee-item {
		display: flex;
		justify-content: space-between;
		margin-bottom: 20rpx;
		text { font-size: 26rpx; color: #7F8C8D; }
		
		&.total {
			margin-top: 30rpx;
			padding-top: 30rpx;
			border-top: 1rpx solid #F2F4F4;
			text { color: #2C3E50; font-weight: bold; }
			.total-price { color: #E74C3C; font-size: 32rpx; }
		}
	}

	.pay-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		.pay-left {
			display: flex;
			align-items: center;
			text { font-size: 28rpx; color: #2C3E50; margin-left: 20rpx; }
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
		justify-content: space-between;
		padding: 0 30rpx;
		border-top: 1rpx solid #EBEEF5;
		
		.total-info {
			text { font-size: 28rpx; color: #2C3E50; }
			.price { font-size: 36rpx; color: #E74C3C; font-weight: bold; }
		}
		
		.submit-btn {
			width: 240rpx;
			height: 80rpx;
			background-color: #2C3E50;
			color: #fff;
			border-radius: 40rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			font-size: 28rpx;
			font-weight: bold;
		}
	}
</style>
