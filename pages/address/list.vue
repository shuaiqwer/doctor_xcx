<template>
	<view class="container">
		<view class="address-list">
			<view class="address-card" v-for="(item, index) in list" :key="index" @click="selectAddress(item)">
				<view class="card-left">
					<view class="user-info">
						<text class="name">{{item.name}}</text>
						<text class="phone">{{item.phone}}</text>
						<text class="tag" v-if="item.isDefault">默认</text>
					</view>
					<view class="address-detail">{{item.province}}{{item.city}}{{item.district}}{{item.detail}}</view>
				</view>
				<view class="card-right">
					<icon type="info" size="18" color="#BDC3C7" />
				</view>
			</view>
		</view>

		<view class="footer-btn">
			<view class="add-btn" @click="addAddress">+ 新增收货地址</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				list: [
					{ 
						name: '张医生', 
						phone: '138****8888', 
						province: '上海市', 
						city: '上海市', 
						district: '静安区', 
						detail: '南京西路1234号 悦容诊所',
						isDefault: true
					},
					{ 
						name: '李院长', 
						phone: '139****9999', 
						province: '北京市', 
						city: '北京市', 
						district: '朝阳区', 
						detail: '建国路88号 华美医疗美容',
						isDefault: false
					}
				]
			}
		},
		methods: {
			selectAddress(item) {
				// 模拟选择地址返回
				uni.navigateBack();
			},
			addAddress() {
				uni.showToast({
					title: '新增地址功能开发中',
					icon: 'none'
				});
			}
		}
	}
</script>

<style lang="scss">
	.container {
		background-color: #F4F7F6;
		min-height: 100vh;
		padding: 20rpx;
	}

	.address-card {
		background-color: #fff;
		border-radius: 20rpx;
		padding: 30rpx;
		margin-bottom: 20rpx;
		display: flex;
		align-items: center;
		
		.card-left {
			flex: 1;
			.user-info {
				display: flex;
				align-items: center;
				margin-bottom: 10rpx;
				.name { font-size: 32rpx; font-weight: bold; color: #2C3E50; margin-right: 20rpx; }
				.phone { font-size: 28rpx; color: #7F8C8D; }
				.tag {
					font-size: 18rpx;
					color: #D4AF37;
					background-color: #FEF5E7;
					padding: 2rpx 10rpx;
					border-radius: 4rpx;
					margin-left: 20rpx;
				}
			}
			.address-detail { font-size: 26rpx; color: #2C3E50; line-height: 36rpx; }
		}
	}

	.footer-btn {
		position: fixed;
		bottom: 40rpx;
		left: 30rpx;
		right: 30rpx;
		.add-btn {
			height: 90rpx;
			background-color: #2C3E50;
			color: #fff;
			border-radius: 45rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			font-size: 30rpx;
			font-weight: bold;
			box-shadow: 0 10rpx 20rpx rgba(44, 62, 80, 0.2);
		}
	}
</style>
