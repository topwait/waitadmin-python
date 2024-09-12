/// <reference types="vite/client" />
import type { Request } from '@/utils/http/request'

declare global {
    const $request: Request
}
