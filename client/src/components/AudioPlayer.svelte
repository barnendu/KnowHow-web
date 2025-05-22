<!-- App.svelte -->
<script>
    import Aplayer from 'svelte-aplayer/dist/svelte/svelte-aplayer.es.js';
    import 'svelte-aplayer/dist/svelte/style.css';
    import TxtViewer from './TxtViewer.svelte';

    export let url ='';
    export let name ='';
    let volume = 0.5
    const audioInfo = {
      name: name,
      artist: '',
      url: url[0],
      cover: 'https://blog-static.fengkx.top/svelte-aplayer/bakemonogatari-ed.jpg',
      lrc: ''
    };
  </script>
  
  <main>
  
    <Aplayer
      audio={JSON.stringify([audioInfo])}
      theme="#e9967a"
      autoplay={true}
      loop="all"
      order="random"
      volume={volume}
      list_folded={false}
    />
    <h2 class="transcript">Full Transcript</h2>
    <TxtViewer url={url[1]} />
  </main>

  <style>
    main {
      overflow-x:auto; 
        height: calc(100vh - 80px);
        box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
        padding: 15px;
    }
    .transcript{
      margin: .5rem 0rem;
    }
  </style>