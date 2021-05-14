<script lang="ts">
	let message = 'Container starting up...';
	const state = {
		files: {
			component: 'files',
			state: 'inactive',
			progress: 0
		},
		scripts: {
			component: 'scripts',
			state: 'inactive',
			progress: 0
		},
		services: {
			component: 'services',
			state: 'inactive',
			progress: 0
		},
		interface: {
			component: 'interface',
			state: 'inactive',
			progress: 0
		},
	};
	const steps = [
		{
			component: 'files',
			svg: 'M16 0H8C6.9 0 6 .9 6 2V18C6 19.1 6.9 20 8 20H20C21.1 20 22 19.1 22 18V6L16 0M20 18H8V2H15V7H20V18M4 4V22H20V24H4C2.9 24 2 23.1 2 22V4H4Z',
		},
		{
			component: 'scripts',
			svg: 'M15,20A1,1 0 0,0 16,19V4H8A1,1 0 0,0 7,5V16H5V5A3,3 0 0,1 8,2H19A3,3 0 0,1 22,5V6H20V5A1,1 0 0,0 19,4A1,1 0 0,0 18,5V9L18,19A3,3 0 0,1 15,22H5A3,3 0 0,1 2,19V18H13A2,2 0 0,0 15,20Z',
		},
		{
			component: 'services',
			svg: 'M12,10L8,14H11V20H13V14H16M19,4H5C3.89,4 3,4.9 3,6V18A2,2 0 0,0 5,20H9V18H5V8H19V18H15V20H19A2,2 0 0,0 21,18V6A2,2 0 0,0 19,4Z',
		},
		{
			component: 'interface',
			svg: 'M4 5V18H21V5H4M6 16V7H9V16H6M11 16V12.5H14V16H11M19 16H16V12.5H19V16M11 10.5V7H19V10.5H11Z',
		},
	];

	let url = window.location.href;
	if (url.startsWith('https://')) {
		url = 'wss://' + url.substring(8);
	} else {
		url = 'ws://' + url.substring(7);
	}
	if (!url.endsWith('/')) {
		url = url +'/websocket';
	} else {
		url = url + 'websocket';
	}
	const webSocket = new WebSocket(url);
	webSocket.onmessage = (ev: MessageEvent) => {
		const data = JSON.parse(ev.data);
		if (data.component) {
			state[data.component] = data;
		} else if (data.message) {
			message = data.message;
		}
	}

	let backoff = 0;
	async function redirectToApp() {
		if (backoff === 0) {
			message = 'Waiting for the interface to become ready...';
			state.interface.state = 'active';
			backoff = 1000;
			setTimeout(redirectToApp, 1000);
		} else {
			try {
				const response = await fetch(window.location.href);
				if (response.status === 200) {
					message = 'Interface ready!';
					state.interface.state = 'complete';
					window.location.reload();
				} else {
					backoff = Math.min(backoff + 1000, 5000);
					setTimeout(redirectToApp, backoff);
				}
			} catch {
				backoff = Math.min(backoff + 1000, 5000);
				setTimeout(redirectToApp, backoff);
			}
		}
	}
	webSocket.onclose = redirectToApp;
</script>

<main>
	<div class="absolute top-1/2 left-1/2 max-w-40 max-h-30 transform -translate-x-1/2 -translate-y-1/2 border-blue border-2 border-solid shadow-lg">
		<h1 class="px-3 py-2 border-gray-200 border-b-2 border-solid font-bold">Container starting up...</h1>
		<ul class="px-3 py-2 flex justify-between">
			{#each steps as step}
				<li>
					<svg viewBox="0 0 24 24" class="w-16 h-16 p-2 sm:w-24 sm:h-24 sm:p-4 fill-current {state[step.component].state === 'complete' ? 'text-green' : (state[step.component].state === 'active' ? 'text-blue animate-pulse' : 'text-gray-300')}">
						<path d={step.svg} />
					</svg>
					{#if state[step.component].state === 'active'}
						<progress min="0" max="100" value={state[step.component].progress} class="w-16 sm:w-24 h-1"/>
					{/if}
				</li>
			{/each}
		</ul>
		<p class="px-3 py-2">{message}</p>
	</div>
</main>

<style global lang="postcss">
	@tailwind base;
	@tailwind components;
	@tailwind utilities;
</style>
