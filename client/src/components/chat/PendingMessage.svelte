<div class="loader">
	<span></span>
	<span></span>
	<span></span>
</div>				

<style>
	.loader {
    text-align: center;
    left:4%;
    position: relative; 
	}
	.loader span {
		display: inline-block;
		vertical-align: middle;
		width: 20px;
		height: 20px;
		background: black;
		border-radius: 20px;
		animation: loader 0.8s infinite alternate;
	}
	.loader span:nth-of-type(2) {
		animation-delay: 0.2s;
	}
	.loader span:nth-of-type(3) {
		animation-delay: 0.6s;
	}
	@keyframes loader {
	0% {
		opacity: 0.9;
		transform: scale(0.5);
	}
	100% {
		opacity: 0.1;
		transform: scale(1);
	}
	}
</style>
