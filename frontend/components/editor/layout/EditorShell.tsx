import Toolbar from "./Toolbar"
import Sidebar from "./Sidebar"
import PreviewPanel from "./PreviewPanel"
import InspectorPanel from "./InspectorPanel"
import TimelinePanel from "./TimelinePanel"

export default function EditorShell() {
  return (
    <div className="h-screen bg-zinc-950 text-white flex flex-col overflow-hidden">
      <Toolbar />

      <div className="flex flex-1 overflow-hidden p-2 gap-2">
        <Sidebar />

        <PreviewPanel />

        <InspectorPanel />
      </div>

      <div className="p-2 pt-0">
        <TimelinePanel />
      </div>
    </div>
  )
}