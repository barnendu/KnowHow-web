<script lang="ts">
    import type { PageData } from './$types';
    import AuthGuard from '$c/AuthGuard.svelte';
    import Grid from 'gridjs-svelte';
    import { h, PluginPosition } from 'gridjs';
    import { goto } from '$app/navigation';
    import { updateDocIdList } from '$s/chat/index';

    const headingPlugin = {
        id: 'heading',
        position: PluginPosition.Header,
        component: () => {
            return h(
                'h1',
                {
                    style: { width: '100%' }
                },
                'Your Documents'
            );
        }
    };

    const className = {
        error: 'error'
    };

    const style = {
        table: {
            width: '100%',
            borderCollapse: 'collapse'
        },
        header: {
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '1rem 0'
        }
    };

    const language = {
        search: {
            placeholder: 'Search documents...'
        }
    };

    const columns = [
        {
            name: '',
            width: '5%',
            formatter: (cell: string, row: any) => {
                const checkBox = h('input', {
                    type: 'checkbox',
                    className: 'w-4 h-4 text-blue-600 rounded focus:ring-blue-500',
                    onClick: () => handleSelectionChange(cell)
                });
                return h('div', { className: 'flex items-center justify-center' }, [checkBox]);
            }
        },
        {
            name: 'Name',
            width: '45%'
        },
        {
            name: 'Date',
            width: '30%'
        },
        {
            name: 'Action',
            width: '20%',
            formatter: (cell: string, row: any) => {
                const chatIcon = h('svg', {
                    className: 'w-5 h-5 mr-1',
                    fill: 'none',
                    stroke: 'currentColor',
                    viewBox: '0 0 24 24',
                    xmlns: 'http://www.w3.org/2000/svg'
                }, [
                    h('path', {
                        'stroke-linecap': 'round',
                        'stroke-linejoin': 'round',
                        'stroke-width': '2',
                        d: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z'
                    })
                ]);

                const campaignIcon = h('svg', {
                    className: 'w-5 h-5 mr-1',
                    fill: 'none',
                    stroke: 'currentColor',
                    viewBox: '0 0 24 24',
                    xmlns: 'http://www.w3.org/2000/svg'
                }, [
                    h('path', {
                        'stroke-linecap': 'round',
                        'stroke-linejoin': 'round',
                        'stroke-width': '2',
                        d: 'M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z'
                    })
                ]);

                const detailsBtn = h(
                    'button',
                    {
                        className: 'btn-primary flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 hover:shadow-md',
                        onClick: () => {
                            updateDocIdList(docList);
                            goto(`/documents/${cell}`);
                        }
                    },
                    [chatIcon, 'Chat']
                );
                const campaignBtn = h(
                    'button',
                    {
                        className: 'btn-secondary flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 hover:shadow-md',
                        onClick: () => goto(`/documents/${cell}?campaign=true`)
                    },
                    [campaignIcon, 'Campaign']
                );

                return h('div', { className: 'flex items-center space-x-2' }, [detailsBtn, campaignBtn]);
            }
        }
    ];

    const server = {
        url: '/api/pdfs',
        total: (data: { count: any }) => data.count,
        then: (data: any[]) =>
            data.map((document: { id: any; name: any; uploaded_on: any }) => [
                document.id,
                document.name,
                document.uploaded_on,
                document.id
            ])
    };

    const pagination = {
        enabled: true,
        limit: 10,
        server: {
            url: (prev: string | string[], page: number) => {
                return `${prev}${prev.includes('?') ? '&' : '?'}page=${page + 1}`;
            }
        }
    };

    const search = {
        enabled: true,
        server: {
            url: (prev: any, keyword: any) => `${prev}?search=${keyword}`
        }
    };

    const docList: string[] = [];
    function handleSelectionChange(docId: string) {
        const index = docList.indexOf(docId);
        if (index !== -1) {
            docList.splice(index, 1);
        } else {
            docList.push(docId);
        }
    }
</script>

<div class="min-h-screen bg-gray-50">
    <AuthGuard />
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
        <div class="bg-white rounded-2xl shadow-sm p-4 sm:p-6 mb-4 sm:mb-6">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 sm:gap-0 mb-6">
                <div>
                    <h2 class="text-xl sm:text-2xl font-bold text-gray-900">Your Documents</h2>
                    <p class="mt-1 text-sm text-gray-500">Manage and interact with your uploaded documents</p>
                </div>
                <a href="/documents/new" class="btn-primary flex items-center px-3 sm:px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 hover:shadow-md w-full sm:w-auto justify-center">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                    </svg>
                    New Document
                </a>
            </div>

            <div class="table-container rounded-xl overflow-x-auto">
                <Grid {search} {columns} {server} {pagination} {language} {className} {style} />
            </div>
        </div>
    </div>
</div>

<style global>
    :root {
        --primary-color: #3b82f6;
        --primary-hover: #2563eb;
        --secondary-color: #6b7280;
        --secondary-hover: #4b5563;
        --background-color: #f9fafb;
        --text-color: #111827;
        --error-color: #ef4444;
    }

    body {
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        background-color: var(--background-color);
        color: var(--text-color);
        margin: 0;
        padding: 0;
    }

    .btn-primary {
        background-color: var(--primary-color);
        color: white;
    }

    .btn-primary:hover {
        background-color: var(--primary-hover);
    }

    .btn-secondary {
        background-color: var(--secondary-color);
        color: white;
    }

    .btn-secondary:hover {
        background-color: var(--secondary-hover);
    }

    :global(.gridjs-container) {
        font-size: 0.875rem;
        border: none !important;
        box-shadow: none !important;
        width: 100% !important;
    }

    :global(.gridjs-wrapper) {
        width: 100% !important;
    }

    :global(.gridjs-table) {
        width: 100% !important;
    }

    :global(.gridjs-header) {
        background-color: #f9fafb !important;
        border-bottom: 1px solid #e5e7eb !important;
        padding: 0.75rem !important;
    }

    :global(.gridjs-th) {
        border: none !important;
        padding: 0.5rem 0.75rem !important;
        font-weight: 600 !important;
        color: #374151 !important;
        white-space: nowrap !important;
    }

    :global(.gridjs-td) {
        border: none !important;
        padding: 0.75rem !important;
        color: #4b5563 !important;
        white-space: nowrap !important;
    }

    @media (max-width: 640px) {
        .table-container {
            overflow-x: auto;
        }
        :global(.gridjs-table) {
            min-width: 600px !important;
        }
        :global(.gridjs-th),
        :global(.gridjs-td) {
            padding: 0.5rem !important;
        }

        :global(.gridjs-pagination) {
            padding: 0.5rem !important;
        }

        :global(.gridjs-pagination .gridjs-pages button) {
            padding: 0.25rem 0.5rem !important;
            font-size: 0.875rem !important;
        }
    }

    :global(.gridjs-pagination) {
        border-top: none !important;
        padding: 1rem !important;
        margin-top: 0 !important;
    }

    :global(.gridjs-pagination .gridjs-pages button) {
        border: 1px solid #e5e7eb !important;
        padding: 0.5rem 1rem !important;
        margin: 0 0.25rem !important;
        border-radius: 0.375rem !important;
    }

    :global(.gridjs-pagination .gridjs-pages button:hover) {
        background-color: #f3f4f6 !important;
    }

    :global(.gridjs-pagination .gridjs-pages button.gridjs-currentPage) {
        background-color: var(--primary-color) !important;
        color: white !important;
        border-color: var(--primary-color) !important;
    }

    :global(.gridjs-search) {
        margin-bottom: 1.5rem !important;
        display: none !important;
    }

    :global(.gridjs-search input) {
        border: 1px solid #e5e7eb !important;
        border-radius: 0.5rem !important;
        padding: 0.75rem 1.25rem !important;
        width: 100% !important;
        font-size: 1rem !important;
        height: 3rem !important;
        background-color: white !important;
        transition: all 0.2s ease-in-out !important;
    }

    :global(.gridjs-search input:focus) {
        outline: none !important;
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        transform: translateY(-1px) !important;
    }

    :global(.gridjs-search input::placeholder) {
        color: #9ca3af !important;
        font-size: 1rem !important;
    }
</style>
