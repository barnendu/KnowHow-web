<script>
// @ts-nocheck

  import { sendMessage } from '$s/chat/index';


export let relatedSearch ="";

function handleRelatedSearch(content) {
    sendMessage({ role: 'user', content, isOpenChat: true }, { useStreaming: true });
}


</script>

<div class="related-section">
    <div style="display:flex">
        <svg width="25px" height="30px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 6H21M3 14H21M17 10H7M17 18H7" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h2>Related</h2>
    </div>
    <ul class="related-list">
     {#each relatedSearch as search}
       
        <li class="related-item"><a on:click={()=>handleRelatedSearch(search.query)}>{search.query}</a> 
                <svg width="15px" height="25px" viewBox="-4 0 20 20" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                    <g id="Free-Icons" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" stroke-linecap="round" stroke-linejoin="round">
                        <g transform="translate(-751.000000, -674.000000)" id="Group" stroke="#000000" stroke-width="2">
                            <g transform="translate(745.000000, 672.000000)" id="Shape">
                                <polyline points="7 3 17.0011615 12.0021033 7 21.0042067">
                
                                </polyline>
                            </g>
                        </g>
                    </g>
                </svg>
            </li>
      {/each}
    </ul>
  </div>

  <style>
    /* Container for the Related section */
    .related-section {
        margin-top: 30px 0px;
        padding: 20px;
        background-color: #f5f5f5;
        border-radius: 5px;
    }

    /* Heading for the Related section */
    .related-section h2 {
        font-size: 20px;
        font-weight: 400;
        margin-bottom: 15px;
        color: #333;
        padding-left: 10px;
    }

    /* List of related items */
    .related-list {
        list-style-type: none;
        padding: 0;
    }

    /* Individual related item */
    .related-item {
        margin-bottom: 10px;
        border-bottom: 1px solid #dcd9d9;
        display: flex;
        padding-bottom: 15px;
        cursor: pointer;
    }

    /* Link for related item */
    .related-item a {
        color: #0b0c0c;
        text-decoration: none;
        transition: color 0.3s ease;
        width: 100%;
    }

    /* Hover effect for related item link */
    .related-item a:hover {
        color: #95989b;
    }
  </style>