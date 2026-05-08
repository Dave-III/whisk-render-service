"use client"

import {
  PanelGroup,
  Panel,
  PanelResizeHandle,
} from "react-resizable-panels"

import Toolbar from "@/components/editor/layout/Toolbar"
import Sidebar from "@/components/editor/layout/Sidebar"
import PreviewPanel from "@/components/editor/layout/PreviewPanel"
import TimelinePanel from "@/components/editor/layout/TimelinePanel"
import InspectorPanel from "@/components/editor/layout/InspectorPanel"

export default function EditorPage() {
  return (
    <div className="h-screen bg-zinc-950 text-white flex flex-col">

      <Toolbar />

      <PanelGroup direction="vertical">

        {/* TOP SECTION */}
        <Panel defaultSize={75} minSize={40}>

          <PanelGroup direction="horizontal">

            {/* SIDEBAR */}
            <Panel defaultSize={18} minSize={12}>
              <Sidebar />
            </Panel>

            <PanelResizeHandle className="w-1 bg-zinc-800 hover:bg-blue-500 transition-colors" />

            {/* PREVIEW */}
            <Panel minSize={30}>
              <PreviewPanel />
            </Panel>

            <PanelResizeHandle className="w-1 bg-zinc-800 hover:bg-blue-500 transition-colors" />

            {/* INSPECTOR */}
            <Panel defaultSize={20} minSize={15}>
              <InspectorPanel />
            </Panel>

          </PanelGroup>

        </Panel>

        <PanelResizeHandle className="h-1 bg-zinc-800 hover:bg-blue-500 transition-colors" />

        {/* TIMELINE */}
        <Panel defaultSize={25} minSize={15}>
          <TimelinePanel />
        </Panel>

      </PanelGroup>

    </div>
  )
}