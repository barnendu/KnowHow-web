<script>
    import { onMount } from 'svelte';
    // @ts-ignore
    import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
    // @ts-ignore
    import { getBlogContent } from '$s/chat';

    import 'ckeditor5/ckeditor5.css';
  
    /**
	 * @type {import("@ckeditor/ckeditor5-editor-classic").ClassicEditor | null}
	 */
    let editorInstance;
    /**
	 * @type {string | HTMLElement}
	 */
    // @ts-ignore
    let editorElement;
    export let blogContent;
    $: reactBlogContent = blogContent;
    onMount(() => {
      ClassicEditor
        // @ts-ignore
        .create(editorElement)
        // @ts-ignore
        .then(editor => {
          editorInstance = editor;
          editor.setData(reactBlogContent);
          sessionStorage.setItem("editor-content", editor.getData());
          editor.model.document.on('change:data', () => {
            console.log('Editor content:', editor.getData());
            sessionStorage.setItem("editor-content", editor.getData());
          });
          editor.editing.view.change(writer => {
              // @ts-ignore
              writer.setStyle('height', '650px', editor.editing.view.document.getRoot());
          });
        })
        // @ts-ignore
        .catch(error => {
          console.error('There was a problem initializing the editor:', error);
        });
  
      return () => {
        // Clean up the editor instance on component destruction
        if (editorInstance) {
          editorInstance.destroy();
          editorInstance = null;
        }
      };
    });
  </script>
  
  <div bind:this={editorElement} class="editor-container"></div>

    
  <style>
  .ck-editor__editable[role="textbox"] {
    min-height: 300px;
    max-height: none;
    overflow-y: visible;
}
  </style>
  