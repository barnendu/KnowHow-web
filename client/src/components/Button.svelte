<script lang="ts">
	import classNames from 'classnames';
	export let disabled = false;
	export let className = '';
</script>

<button
	type="submit"
	class={classNames(
		'py-3 px-4 inline-flex justify-center items-center gap-2 rounded-md border border-transparent font-semibold bg-blue text-white hover:bg-blue focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all text-sm dark:focus:ring-offset-gray-800',
		className
	)}
	{disabled}><slot /></button
>
<style>
	.bg-blue{
		background-color: rgb(27, 3, 106)
	}
</style>
