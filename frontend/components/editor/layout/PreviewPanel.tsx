export default function PreviewPanel() {
  return (
    <div className="flex-1 p-4 flex items-center justify-center">
      <div className="aspect-video w-full max-w-4xl bg-black rounded-lg border border-zinc-800 flex items-center justify-center">
        <span className="text-zinc-500 text-sm">
          Video Preview
        </span>
      </div>
    </div>
  )
}