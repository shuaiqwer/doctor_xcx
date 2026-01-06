<template>
	<view class="container">
		<view class="login-header">
			<image class="logo" src="/static/logo.png" mode="aspectFit"></image>
			<text class="title">悦容美药</text>
			<text class="subtitle">专业医美药品直供平台</text>
		</view>

		<view class="login-form">
			<view class="input-group">
				<text class="label">OpenID (从抓包获取)</text>
				<input class="input" v-model="ssoParams.openId" placeholder="请输入 openId" />
			</view>
			<view class="input-group">
				<text class="label">加密用户名 (userName)</text>
				<input class="input" v-model="ssoParams.userName" placeholder="请输入加密后的 userName" />
			</view>
			
			<button class="login-btn" @click="handleSsoLogin">使用 SSO 参数登录</button>
			
			<view class="divider">
				<text>或者</text>
			</view>
			
			<button class="wechat-btn" @click="getWechatCode">
				<icon type="success" size="18" color="#fff" />
				<text>获取微信 Login Code</text>
			</button>
			
			<view v-if="loginCode" class="code-box">
				<text class="code-label">当前 Code (有效期5分钟):</text>
				<text class="code-value" selectable>{{ loginCode }}</text>
				<button class="copy-btn" size="mini" @click="copyCode">复制 Code</button>
			</view>
		</view>
		
		<view class="tips">
			<text>提示：由于小程序环境限制，OpenID 需要通过抓包工具（如 Charles/Fiddler）从官方小程序的 jwtToken 接口请求中获取。</text>
		</view>
	</view>
</template>

<script>
	import { apiService } from '@/utils/api.js';

	export default {
		data() {
			return {
				ssoParams: {
					openId: uni.getStorageSync('debug_openId') || 'oNhz74qWS-UMvJulMhKGDSTMXaYg',
					userName: uni.getStorageSync('debug_userName') || '1K/9Mne22mOa2NVPlG0ekg=='
				},
				loginCode: ''
			}
		},
		methods: {
			async handleSsoLogin() {
				if (!this.ssoParams.openId || !this.ssoParams.userName) {
					return uni.showToast({ title: '请填写完整参数', icon: 'none' });
				}
				
				// 保存到本地方便下次使用
				uni.setStorageSync('debug_openId', this.ssoParams.openId);
				uni.setStorageSync('debug_userName', this.ssoParams.userName);
				
				uni.showLoading({ title: '正在登录...' });
				try {
					// 这里我们临时修改 apiService 的参数
					// 实际开发中可以把这些参数存入 storage，让 apiService 自动读取
					const jwt = await apiService.autoLogin();
					uni.hideLoading();
					uni.showToast({ title: '登录成功', icon: 'success' });
					setTimeout(() => {
						uni.switchTab({ url: '/pages/index/index' });
					}, 1500);
				} catch (e) {
					uni.hideLoading();
					uni.showModal({
						title: '登录失败',
						content: e.message,
						showCancel: false
					});
				}
			},
			getWechatCode() {
				uni.login({
					provider: 'weixin',
					success: (res) => {
						this.loginCode = res.code;
						console.log('获取到微信 Code:', res.code);
					},
					fail: (err) => {
						uni.showToast({ title: '获取 Code 失败', icon: 'none' });
					}
				});
			},
			copyCode() {
				uni.setClipboardData({
					data: this.loginCode,
					success: () => {
						uni.showToast({ title: '已复制到剪贴板' });
					}
				});
			}
		}
	}
</script>

<style lang="scss">
	.container {
		padding: 60rpx 40rpx;
		background-color: #fff;
		min-height: 100vh;
	}
	
	.login-header {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-bottom: 80rpx;
		
		.logo {
			width: 160rpx;
			height: 160rpx;
			margin-bottom: 20rpx;
		}
		
		.title {
			font-size: 44rpx;
			font-weight: bold;
			color: #2C3E50;
			margin-bottom: 10rpx;
		}
		
		.subtitle {
			font-size: 26rpx;
			color: #7F8C8D;
		}
	}
	
	.login-form {
		.input-group {
			margin-bottom: 30rpx;
			
			.label {
				font-size: 24rpx;
				color: #7F8C8D;
				margin-bottom: 10rpx;
				display: block;
			}
			
			.input {
				height: 90rpx;
				background-color: #F4F7F6;
				border-radius: 12rpx;
				padding: 0 30rpx;
				font-size: 28rpx;
			}
		}
		
		.login-btn {
			background-color: #2C3E50;
			color: #fff;
			height: 90rpx;
			line-height: 90rpx;
			border-radius: 12rpx;
			font-size: 32rpx;
			margin-top: 40rpx;
		}
		
		.divider {
			display: flex;
			align-items: center;
			margin: 40rpx 0;
			
			&::before, &::after {
				content: '';
				flex: 1;
				height: 1rpx;
				background-color: #EBEEF5;
			}
			
			text {
				padding: 0 20rpx;
				font-size: 24rpx;
				color: #909399;
			}
		}
		
		.wechat-btn {
			background-color: #07C160;
			color: #fff;
			height: 90rpx;
			line-height: 90rpx;
			border-radius: 12rpx;
			font-size: 32rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			
			text {
				margin-left: 10rpx;
			}
		}
	}
	
	.code-box {
		margin-top: 30rpx;
		padding: 20rpx;
		background-color: #F0F9EB;
		border: 1rpx solid #E1F3D8;
		border-radius: 8rpx;
		
		.code-label {
			font-size: 22rpx;
			color: #67C23A;
			display: block;
		}
		
		.code-value {
			font-size: 28rpx;
			color: #2C3E50;
			word-break: break-all;
			margin: 10rpx 0;
			display: block;
		}
		
		.copy-btn {
			margin-top: 10rpx;
		}
	}
	
	.tips {
		margin-top: 60rpx;
		font-size: 22rpx;
		color: #909399;
		line-height: 1.6;
	}
</style>
