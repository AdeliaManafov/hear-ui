type ToastOptions = {
  title?: string
  description?: string
  type?: "success" | "error" | "info"
}

export const toaster = {
  create: (opts: ToastOptions) => {
    // Minimal placeholder for build-time. In the real app replace with a proper UI toast.
    // This keeps imports working while the Vue UI is implemented.
    // eslint-disable-next-line no-console
    console.log("TOAST", opts.title, opts.description, opts.type)
  },
}

export default toaster
