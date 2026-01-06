<template>
	<view class="container">
		<!-- 顶部背景 -->
		<view class="user-header">
			<view class="user-card">
				<view class="avatar-box">
					<view class="avatar-placeholder"></view>
				</view>
				<view class="user-info">
					<text class="nickname">悦容尊享会员</text>
					<view class="level-badge" :style="{ background: memberLevel.bg, color: memberLevel.textColor, border: memberLevel.border }">
						<text>{{memberLevel.name}}</text>
					</view>
				</view>
				<view class="settings-icon">
					<icon type="waiting" size="20" color="#fff" />
				</view>
			</view>
		</view>

		<!-- 会员卡片 -->
		<view class="vip-card-wrapper">
			<view class="vip-card" @click="goToMember">
				<view class="vip-left">
					<view class="vip-title">
						<text class="gold-text">悦容黑金会员</text>
						<view class="vip-tag">VIP</view>
					</view>
					<text class="vip-desc">专享会员价 · 积分抵现 · 优先发货</text>
				</view>
				<view class="vip-right">
					<text class="btn-text">立即查看</text>
				</view>
			</view>
		</view>

		<!-- 资产简报 -->
		<view class="assets-section">
			<view class="assets-row">
				<view class="asset-item" @click="showToast('积分商城开发中')">
					<text class="num">1,280</text>
					<text class="label">可用积分</text>
				</view>
				<view class="asset-item" @click="showToast('暂无优惠券')">
					<text class="num">3</text>
					<text class="label">优惠券</text>
				</view>
				<view class="asset-item" @click="showToast('余额：￥0.00')">
					<text class="num">0.00</text>
					<text class="label">账户余额</text>
				</view>
			</view>
		</view>

		<!-- 订单管理 -->
		<view class="menu-section order-section">
			<view class="section-header" @click="goToOrders(0)">
				<text class="title">我的订单</text>
				<text class="more">全部订单 ></text>
			</view>
			<view class="order-grid">
				<view class="order-item" @click="goToOrders(1)">
					<view class="icon-placeholder"></view>
					<text>待付款</text>
				</view>
				<view class="order-item" @click="goToOrders(2)">
					<view class="icon-placeholder"></view>
					<text>待发货</text>
				</view>
				<view class="order-item" @click="goToOrders(3)">
					<view class="icon-placeholder"></view>
					<text>待收货</text>
				</view>
				<view class="order-item" @click="goToOrders(4)">
					<view class="icon-placeholder"></view>
					<text>评价</text>
				</view>
			</view>
		</view>

		<!-- 权威认证/服务 -->
		<view class="menu-section">
			<view class="menu-list">
				<view class="menu-item" @click="showToast('资质认证开发中')">
					<view class="menu-left">
						<icon type="success" size="18" color="#2C3E50" />
						<text>资质认证</text>
					</view>
					<text class="menu-right">去认证</text>
				</view>
				<view class="menu-item" @click="showToast('溯源查询开发中')">
					<view class="menu-left">
						<icon type="search" size="18" color="#2C3E50" />
						<text>正品溯源查询</text>
					</view>
					<text class="menu-right"></text>
				</view>
				<view class="menu-item" @click="goToAddress">
					<view class="menu-left">
						<icon type="download" size="18" color="#2C3E50" />
						<text>收货地址</text>
					</view>
					<text class="menu-right"></text>
				</view>
				<view class="menu-item" @click="showToast('联系客服')">
					<view class="menu-left">
						<icon type="contact" size="18" color="#2C3E50" />
						<text>在线客服</text>
					</view>
					<text class="menu-right">9:00-21:00 </text>
				</view>
			</view>
		</view>
		
		<view class="version-info">
			<text>悦容美药 v1.0.0</text>
			<text>专业医美药品直供平台</text>
		</view>
	</view>
</template>

<script>
	import { apiService, MEMBER_LEVELS } from '@/utils/api.js';

	export default {
		data() {
			return {
				memberLevel: {}
			}
		},
		onLoad() {
			const levelKey = apiService.getCurrentMemberLevel();
			this.memberLevel = MEMBER_LEVELS[levelKey];
		},
		methods: {
			goToOrders(index) {
				uni.navigateTo({
					url: '/pages/order/list?type=' + index
				});
			},
			goToAddress() {
				uni.navigateTo({
					url: '/pages/address/list'
				});
			},
			goToMember() {
				uni.navigateTo({
					url: '/pages/mine/member'
				});
			},
			goToLogin() {
				uni.navigateTo({
					url: '/pages/login/login'
				});
			},
			async handleAutoLogin() {
				uni.showLoading({ title: '正在登录...' });
				try {
					const jwt = await apiService.autoLogin();
					uni.hideLoading();
					uni.showToast({
						title: '登录成功',
						icon: 'success'
					});
					console.log('手动触发登录成功，新 JWT:', jwt);
				} catch (e) {
					uni.hideLoading();
					uni.showModal({
						title: '登录失败',
						content: e.message || '请检查网络或联系管理员',
						showCancel: false
					});
				}
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
		min-height: 100vh;
	}

	.user-header {
		background-color: #2C3E50;
		padding: 60rpx 30rpx 100rpx;
		position: relative;
		
		.user-card {
			display: flex;
			align-items: center;
			margin-bottom: 40rpx;
		}
		
		.avatar-box {
			width: 120rpx;
			height: 120rpx;
			border-radius: 60rpx;
			background-color: #fff;
			padding: 4rpx;
			margin-right: 30rpx;
			
			.avatar-placeholder {
				width: 100%;
				height: 100%;
				border-radius: 50%;
				background-color: #EBEEF5;
			}
		}
		
		.nickname {
			font-size: 36rpx;
			color: #fff;
			font-weight: bold;
			display: block;
			margin-bottom: 10rpx;
		}
		
		.level-badge {
			display: inline-flex;
			align-items: center;
			padding: 4rpx 20rpx;
			border-radius: 20rpx;
			font-size: 20rpx;
			font-weight: bold;
			box-shadow: 0 4rpx 8rpx rgba(0,0,0,0.1);
		}
		
		.settings-icon {
			margin-left: auto;
		}
	}

	.vip-card-wrapper {
		margin: -60rpx 30rpx 0;
		position: relative;
		z-index: 2;
		
		.vip-card {
			background: linear-gradient(135deg, #3D3D3D 0%, #1A1A1A 100%);
			border-radius: 20rpx;
			padding: 30rpx 40rpx;
			display: flex;
			justify-content: space-between;
			align-items: center;
			box-shadow: 0 10rpx 30rpx rgba(0,0,0,0.2);
			border: 1rpx solid rgba(212, 175, 55, 0.3);
			
			.vip-title {
				display: flex;
				align-items: center;
				margin-bottom: 10rpx;
				
				.gold-text {
					font-size: 32rpx;
					color: #D4AF37;
					font-weight: bold;
					letter-spacing: 2rpx;
				}
				
				.vip-tag {
					background-color: #D4AF37;
					color: #1A1A1A;
					font-size: 18rpx;
					font-weight: bold;
					padding: 2rpx 8rpx;
					border-radius: 4rpx;
					margin-left: 15rpx;
				}
			}
			
			.vip-desc {
				font-size: 22rpx;
				color: rgba(212, 175, 55, 0.7);
			}
			
			.vip-right {
				background: linear-gradient(90deg, #D4AF37 0%, #F1C40F 100%);
				padding: 10rpx 24rpx;
				border-radius: 30rpx;
				
				.btn-text {
					font-size: 22rpx;
					color: #1A1A1A;
					font-weight: bold;
				}
			}
		}
	}

	.assets-section {
		margin: 20rpx 30rpx;
		background-color: #fff;
		border-radius: 20rpx;
		padding: 30rpx 0;
		box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.05);
		
		.assets-row {
			display: flex;
			justify-content: space-around;
			
			.asset-item {
				display: flex;
				flex-direction: column;
				align-items: center;
				flex: 1;
				border-right: 1rpx solid #F2F4F4;
				
				&:last-child {
					border-right: none;
				}
				
				.num {
					font-size: 32rpx;
					color: #2C3E50;
					font-weight: bold;
					margin-bottom: 8rpx;
				}
				
				.label {
					font-size: 22rpx;
					color: #7F8C8D;
				}
			}
		}
	}

	.menu-section {
		margin: 0 30rpx 20rpx;
		background-color: #fff;
		border-radius: 20rpx;
		padding: 30rpx;
		box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.05);
		
		&.order-section {
			margin-top: 0;
		}
		
		.section-header {
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-bottom: 30rpx;
			padding-bottom: 20rpx;
			border-bottom: 1rpx solid #F2F4F4;
			
			.title {
				font-size: 30rpx;
				font-weight: bold;
				color: #2C3E50;
			}
			
			.more {
				font-size: 24rpx;
				color: #BDC3C7;
			}
		}
	}

	.order-grid {
		display: flex;
		justify-content: space-around;
		
		.order-item {
			display: flex;
			flex-direction: column;
			align-items: center;
			
			.icon-placeholder {
				width: 48rpx;
				height: 48rpx;
				background-color: #F2F4F4;
				border-radius: 10rpx;
				margin-bottom: 15rpx;
			}
			
			text {
				font-size: 24rpx;
				color: #7F8C8D;
			}
		}
	}

	.menu-list {
		.menu-item {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 30rpx 0;
			border-bottom: 1rpx solid #F2F4F4;
			
			&:last-child {
				border-bottom: none;
			}
			
			.menu-left {
				display: flex;
				align-items: center;
				
				text {
					font-size: 28rpx;
					color: #2C3E50;
					margin-left: 20rpx;
				}
			}
			
			.menu-right {
				font-size: 24rpx;
				color: #BDC3C7;
			}
		}
	}
	
	.version-info {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 60rpx 0;
		
		text {
			font-size: 22rpx;
			color: #BDC3C7;
			line-height: 36rpx;
		}
	}
</style>
