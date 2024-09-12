import useUserStore from '@/stores/modules/user'

export default {
    mounted: (el: HTMLElement, binding: any): void => {
        const { value } = binding
        const userStore = useUserStore()
        const permissions = userStore.perms
        const allPermission: string = '*'

        if (Array.isArray(value)) {
            if (value.length > 0) {
                const hasPermission = permissions.some((key: string) => {
                    return allPermission === key || value.includes(key)
                })

                const hide: boolean = false
                if (!hasPermission) {
                    if (hide) {
                        el && el.removeChild(el)
                    } else {
                        el && el.classList.add('is-disabled')
                        el && el.setAttribute('aria-disabled', 'true')
                        el && el.setAttribute('disabled', 'true')
                    }
                }
            }
        } else {
            throw new Error('Error: v-perms="[\'auth:admin:add\']"')
        }
    }
}
