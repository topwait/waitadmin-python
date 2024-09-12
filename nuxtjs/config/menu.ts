const menus: any = [
    {
        'name': '首页',
        'path': '/',
        'target': '_self'
    },
    {
        'name': '文章资讯',
        'path': '/article/lists',
        'target': '_self'
    },
    {
        'name': '开发手册',
        'path': 'https://www.waitadmin.cn/docs/python/',
        'target': '_blank'
    },
    {
        'name': '源码下载',
        'path': 'javascript:',
        'children': [
            {
                'name': 'Github',
                'path': 'https://www.waitadmin.cn',
                'target': '_blank'
            },
            {
                'name': 'Gitee',
                'path': 'https://www.waitadmin.cn',
                'target': '_blank'
            },
        ]
    }
]

export default menus
