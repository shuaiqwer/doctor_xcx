<template>
	<view class="container">
		<!-- 会员卡展示 -->
		<view class="member-card-box">
			<view class="member-card black-gold">
				<view class="card-header">
					<view class="brand">
						<text class="name">悦容美药 · 尊享会员</text>
						<text class="en">PREMIUM MEMBER</text>
					</view>
					<view class="vip-logo">VIP</view>
				</view>
				<view class="card-body">
					<view class="user-info">
						<view class="avatar-placeholder"></view>
						<view class="info">
							<text class="nickname">未登录用户</text>
							<text class="level">黑金会员 · 永久有效</text>
						</view>
					</view>
				</view>
				<view class="card-footer">
					<text class="points">当前积分：1,280</text>
					<text class="code">NO.8888 6666</text>
				</view>
			</view>
		</view>

		<!-- 会员权益 -->
		<view class="section">
			<view class="section-title">会员尊享权益</view>
			<view class="privilege-grid">
				<view class="privilege-item" v-for="(item, index) in privileges" :key="index">
					<view class="icon-box" :style="{ backgroundColor: item.bg }">
						<icon :type="item.icon" size="24" color="#D4AF37" />
					</view>
					<text class="p-name">{{item.name}}</text>
					<text class="p-desc">{{item.desc}}</text>
				</view>
			</view>
		</view>

		<!-- 等级说明 -->
		<view class="section">
			<view class="section-title">会员等级体系</view>
			<view class="level-list">
				<view class="level-item" v-for="(level, index) in levels" :key="index">
					<view class="level-info">
						<text class="l-name">{{level.name}}</text>
						<text class="l-req">{{level.req}}</text>
					</view>
					<view class="level-benefits">
						<text class="b-tag" v-for="(b, bIdx) in level.benefits" :key="bIdx">{{b}}</text>
					</view>
				</view>
			</view>
		</view>

		<!-- 积分任务 -->
		<view class="section">
			<view class="section-title">赚取积分</view>
			<view class="task-list">
				<view class="task-item" v-for="(task, index) in tasks" :key="index">
					<view class="task-info">
						<text class="t-name">{{task.name}}</text>
						<text class="t-reward">+{{task.reward}} 积分</text>
					</view>
					<view class="task-btn" :class="{ done: task.done }">{{task.done ? '已完成' : '去完成'}}</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				privileges: [
					{ name: '会员专享价', desc: '全场药品95折起', icon: 'success', bg: '#FEF5E7' },
					{ name: '积分抵现', desc: '100积分抵1元', icon: 'info', bg: '#EBF5FB' },
					{ name: '优先发货', desc: '订单优先处理', icon: 'waiting', bg: '#EAFAF1' },
					{ name: '专属客服', desc: '1对1医美顾问', icon: 'contact', bg: '#F4ECF7' }
				],
				levels: [
					{ name: '普通会员', req: '注册即可加入', benefits: ['积分累计', '正品溯源'] },
					{ name: '白银会员', req: '消费满1,000元', benefits: ['98折优惠', '生日礼包'] },
					{ name: '黄金会员', req: '消费满5,000元', benefits: ['95折优惠', '双倍积分'] },
					{ name: '黑金会员', req: '消费满20,000元', benefits: ['9折优惠', '顺丰包邮', '专属顾问'] }
				],
				tasks: [
					{ name: '每日签到', reward: 10, done: false },
					{ name: '完善个人资料', reward: 50, done: true },
					{ name: '首次购买药品', reward: 200, done: true },
					{ name: '分享给好友', reward: 30, done: false }
				]
			}
		}
	}
</script>

<style lang="scss">
	.container {
		background-color: #F4F7F6;
		min-height: 100vh;
		padding: 30rpx;
	}

	.member-card-box {
		margin-bottom: 40rpx;
		
		.member-card {
			height: 360rpx;
			border-radius: 30rpx;
			padding: 40rpx;
			display: flex;
			flex-direction: column;
			justify-content: space-between;
			position: relative;
			overflow: hidden;
			box-shadow: 0 20rpx 40rpx rgba(0,0,0,0.15);
			
			&.black-gold {
				background: linear-gradient(135deg, #3D3D3D 0%, #1A1A1A 100%);
				border: 1rpx solid rgba(212, 175, 55, 0.3);
			}
			
			.card-header {
				display: flex;
				justify-content: space-between;
				align-items: flex-start;
				
				.brand {
					display: flex;
					flex-direction: column;
					.name { font-size: 32rpx; color: #D4AF37; font-weight: bold; }
					.en { font-size: 18rpx; color: rgba(212, 175, 55, 0.5); letter-spacing: 2rpx; }
				}
				
				.vip-logo {
					font-size: 48rpx;
					font-weight: bold;
					color: rgba(212, 175, 55, 0.2);
					font-style: italic;
				}
			}
			
			.user-info {
				display: flex;
				align-items: center;
				
				.avatar-placeholder {
					width: 100rpx;
					height: 100rpx;
					border-radius: 50%;
					background-color: rgba(255,255,255,0.1);
					border: 2rpx solid #D4AF37;
					margin-right: 20rpx;
				}
				
				.info {
					.nickname { font-size: 34rpx; color: #fff; font-weight: bold; display: block; margin-bottom: 6rpx; }
					.level { font-size: 24rpx; color: #D4AF37; }
				}
			}
			
			.card-footer {
				display: flex;
				justify-content: space-between;
				align-items: flex-end;
				.points { font-size: 26rpx; color: #D4AF37; }
				.code { font-size: 22rpx; color: rgba(255,255,255,0.3); font-family: monospace; }
			}
		}
	}

	.section {
		background-color: #fff;
		border-radius: 20rpx;
		padding: 30rpx;
		margin-bottom: 30rpx;
		
		.section-title {
			font-size: 30rpx;
			font-weight: bold;
			color: #2C3E50;
			margin-bottom: 30rpx;
			position: relative;
			padding-left: 20rpx;
			
			&::before {
				content: '';
				position: absolute;
				left: 0;
				top: 50%;
				transform: translateY(-50%);
				width: 6rpx;
				height: 28rpx;
				background-color: #D4AF37;
				border-radius: 4rpx;
			}
		}
	}

	.privilege-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 20rpx;
		
		.privilege-item {
			padding: 20rpx;
			background-color: #F8F9F9;
			border-radius: 16rpx;
			display: flex;
			flex-direction: column;
			align-items: center;
			text-align: center;
			
			.icon-box {
				width: 80rpx;
				height: 80rpx;
				border-radius: 40rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				margin-bottom: 15rpx;
			}
			
			.p-name { font-size: 26rpx; color: #2C3E50; font-weight: bold; margin-bottom: 6rpx; }
			.p-desc { font-size: 20rpx; color: #7F8C8D; }
		}
	}

	.level-list {
		.level-item {
			padding: 20rpx 0;
			border-bottom: 1rpx solid #F2F4F4;
			&:last-child { border-bottom: none; }
			
			.level-info {
				display: flex;
				justify-content: space-between;
				margin-bottom: 15rpx;
				.l-name { font-size: 28rpx; color: #2C3E50; font-weight: bold; }
				.l-req { font-size: 24rpx; color: #7F8C8D; }
			}
			
			.level-benefits {
				display: flex;
				flex-wrap: wrap;
				.b-tag {
					font-size: 20rpx;
					color: #D4AF37;
					background-color: #FEF5E7;
					padding: 4rpx 16rpx;
					border-radius: 20rpx;
					margin-right: 15rpx;
					margin-bottom: 10rpx;
				}
			}
		}
	}

	.task-list {
		.task-item {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 25rpx 0;
			border-bottom: 1rpx solid #F2F4F4;
			&:last-child { border-bottom: none; }
			
			.task-info {
				.t-name { font-size: 28rpx; color: #2C3E50; display: block; margin-bottom: 6rpx; }
				.t-reward { font-size: 24rpx; color: #D4AF37; font-weight: bold; }
			}
			
			.task-btn {
				font-size: 24rpx;
				color: #fff;
				background-color: #2C3E50;
				padding: 10rpx 30rpx;
				border-radius: 30rpx;
				
				&.done {
					background-color: #EBEEF5;
					color: #BDC3C7;
				}
			}
		}
	}
</style>