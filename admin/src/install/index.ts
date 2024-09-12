import type { App } from 'vue'

const modules: Record<string, any> = import.meta.glob('./**/*', { eager: true })

function install(app: App<Element>): void {
    Object.keys(modules).forEach((key: string): void => {
        const name: string = key.replace(/(.*\/)*([^.]+).*/gi, '$2')
        const type: string = key.replace(/^\.\/([\w-]+).*/gi, '$1')
        const module: any = modules[key]
        if (module.default) {
            switch (type) {
                case 'directives':
                    app.directive(name, module.default)
                    break
                case 'plugins':
                    typeof module.default === 'function' && module.default(app)
                    break
            }
        }
    })
}

export default {
    install
}
