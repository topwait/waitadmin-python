import { createRequest } from '~~/utils/http'

export default defineNuxtPlugin((): void => {
    (globalThis as any).$request = createRequest()
})
