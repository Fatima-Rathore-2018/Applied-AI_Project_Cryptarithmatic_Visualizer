import CryptarithmeticVisualizer from "@/components/cryptarithmetic-visualizer"

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <CryptarithmeticVisualizer />
      </div>
    </main>
  )
}
