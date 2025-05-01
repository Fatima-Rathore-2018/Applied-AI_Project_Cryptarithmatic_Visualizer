"use client"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Slider } from "@/components/ui/slider"
import { Card } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { motion } from "framer-motion"
import { Play, Pause, RotateCcw, Plus, Equal, Sparkles, X, Calculator, SkipForward } from "lucide-react"

type LetterMapping = {
  [key: string]: number | null
}

type SolutionStep = {
  message: string
  mapping: LetterMapping
  domains: { [key: string]: number[] }
  currentLetter?: string
  currentValue?: number | null
  isValid?: boolean
  assign?: string
  value?: number
  current?: { [key: string]: number }
  stepType?: string
  equationsUsed?: number[]
}

// Color palette for digits
const DIGIT_COLORS = [
  "bg-rose-500", // 0
  "bg-pink-500", // 1
  "bg-purple-500", // 2
  "bg-violet-500", // 3
  "bg-indigo-500", // 4
  "bg-blue-500", // 5
  "bg-cyan-500", // 6
  "bg-teal-500", // 7
  "bg-emerald-500", // 8
  "bg-green-500", // 9
]

// Add a helper to build query string for EventSource
function buildQuery(params: Record<string, string>) {
  return (
    '?' +
    Object.entries(params)
      .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
      .join('&')
  )
}

// ClientOnly component to prevent hydration errors with random rendering
function ClientOnly({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  if (!mounted) return null;
  return <>{children}</>;
}

export default function CryptarithmeticVisualizer() {
  const [firstWord, setFirstWord] = useState("")
  const [secondWord, setSecondWord] = useState("")
  const [resultWord, setResultWord] = useState("")
  const [speed, setSpeed] = useState(50)
  const [isRunning, setIsRunning] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [solution, setSolution] = useState<LetterMapping | null>(null)
  const [steps, setSteps] = useState<SolutionStep[]>([])
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState("input")
  const [digitToLetters, setDigitToLetters] = useState<{ [key: number]: string[] }>({})
  const [uniqueLetters, setUniqueLetters] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [equations, setEquations] = useState<string[]>([])
  const [isClient, setIsClient] = useState(false)
  const [mounted, setMounted] = useState(false)
  const [eventSource, setEventSource] = useState<EventSource | null>(null)
  const [isFinished, setIsFinished] = useState(false)
  const [isSuccess, setIsSuccess] = useState(false)

  // Reset the visualization
  const resetVisualization = () => {
    setIsRunning(false)
    setCurrentStep(0)
    setSolution(null)
    setSteps([])
    setError(null)
    setActiveTab("input")
    setDigitToLetters({})
    setIsLoading(false)
    setEquations([])
  }

  // Update digit to letters mapping
  const updateDigitToLetters = (mapping: LetterMapping) => {
    const result: { [key: number]: string[] } = {}

    Object.entries(mapping).forEach(([letter, digit]) => {
      if (digit !== null) {
        if (!result[digit]) {
          result[digit] = []
        }
        result[digit].push(letter)
      }
    })

    setDigitToLetters(result)
  }

  // Start or pause the visualization
  const toggleVisualization = () => {
    if (steps.length === 0) {
      handleSolveButtonClick()
    }
    setIsRunning(!isRunning)
  }

  // Skip to the next step
  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1)
      updateDigitToLetters(steps[currentStep + 1]?.mapping || {})
    }
  }

  // Skip to the end of the visualization
  const skipToEnd = () => {
    if (steps.length > 0) {
      setCurrentStep(steps.length - 1)
      setIsRunning(false)
      updateDigitToLetters(steps[steps.length - 1]?.mapping || {})
    }
  }

  // Advance the visualization based on the speed
  useEffect(() => {
    if (!isRunning || steps.length === 0 || currentStep >= steps.length - 1) {
      setIsRunning(false)
      return
    }

    const interval = setInterval(
      () => {
        setCurrentStep((prev) => {
          const next = prev + 1
          if (next >= steps.length - 1) {
            setIsRunning(false)
            return steps.length - 1
          }
          return next
        })

        // Update digit to letters mapping
        updateDigitToLetters(steps[currentStep + 1]?.mapping || {})
      },
      1000 - speed * 9,
    ) // Speed ranges from 100ms to 1000ms

    return () => clearInterval(interval)
  }, [isRunning, currentStep, steps.length, speed])

  useEffect(() => {
    setIsClient(true)
    setMounted(true)
  }, [])

  // Clean up EventSource on unmount
  useEffect(() => {
    setMounted(true)
    return () => {
      if (eventSource) eventSource.close()
    }
  }, [])

  // Format the equation with the current mapping
  const formatEquation = (mapping: LetterMapping = {}) => {
    const formatWord = (word: string) => {
      return word.split("").map((letter, index) => {
        const value = mapping[letter]
        const digitColor = value !== null ? DIGIT_COLORS[value] : "bg-gray-200 dark:bg-gray-700"

        return (
          <motion.div
            key={index}
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.3, delay: index * 0.05 }}
            className="relative"
          >
            <div
              className={`w-16 h-16 m-1 rounded-xl flex items-center justify-center shadow-lg ${
                value !== null ? digitColor : "bg-gray-200 dark:bg-gray-700"
              }`}
            >
              <span className="text-3xl font-bold text-white">{value !== null ? value : letter}</span>
            </div>
            {value !== null && (
              <div className="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-white dark:bg-gray-800 flex items-center justify-center shadow-sm">
                <span className="text-xs font-bold">{letter}</span>
              </div>
            )}
          </motion.div>
        )
      })
    }

    return (
      <div className="flex flex-col items-center space-y-6 my-8">
        <div className="flex items-center">
          <div className="flex">{formatWord(firstWord)}</div>
        </div>
        <div className="flex items-center">
          <div className="w-8 mr-2">
            <Plus className="w-8 h-8 text-pink-400" />
          </div>
          <div className="flex">{formatWord(secondWord)}</div>
        </div>
        <div className="w-full max-w-md border-t-2 border-purple-400 my-2"></div>
        <div className="flex items-center">
          <div className="w-8 mr-2">
            <Equal className="w-8 h-8 text-purple-400" />
          </div>
          <div className="flex">{formatWord(resultWord)}</div>
        </div>
      </div>
    )
  }

  // Check if the current mapping makes the equation valid
  const isEquationValid = (mapping: LetterMapping) => {
    // Check if all letters have been assigned
    const allLetters = [...new Set([...firstWord, ...secondWord, ...resultWord])]
    if (allLetters.some((letter) => mapping[letter] === undefined || mapping[letter] === null)) {
      return false
    }

    // Convert words to numbers
    const num1 = Number.parseInt(
      firstWord
        .split("")
        .map((l) => mapping[l])
        .join(""),
    )
    const num2 = Number.parseInt(
      secondWord
        .split("")
        .map((l) => mapping[l])
        .join(""),
    )
    const result = Number.parseInt(
      resultWord
        .split("")
        .map((l) => mapping[l])
        .join(""),
    )

    return num1 + num2 === result
  }

  // Render the decision tree
  const renderDecisionTree = () => {
    if (!steps[currentStep]) return null;

    const mapping = steps[currentStep].mapping || {}; // Ensure mapping is an object
    const assignedLetters = Object.entries(mapping)
        .filter(([_, value]) => value !== null)
        .map(([letter, value]) => ({ letter, value }));

    return (
        <div className="flex flex-col items-center space-y-4 mt-4">
            <h3 className="text-lg font-medium text-white">Decision Tree Visualization</h3>
            <div className="flex flex-col items-center space-y-2">
                {assignedLetters.map(({ letter, value }, index) => (
                    <div key={index} className="flex flex-col items-center">
                        <div className="w-40 h-12 bg-sky-200 rounded-md flex items-center justify-center text-slate-800 font-bold">
                            {letter}={value}
                        </div>
                        {index < assignedLetters.length - 1 && <div className="h-6 w-0.5 bg-gray-400"></div>}
                    </div>
                ))}
            </div>
        </div>
    );
  }

  // Render the domains
  const renderDomains = () => {
    if (!steps[currentStep]?.domains) return null

    // Get previous step domains for comparison
    const prevDomains = currentStep > 0 ? steps[currentStep - 1]?.domains : null

    return (
      <div className="mt-4">
        <h3 className="text-lg font-medium text-white mb-2">Current Domains:</h3>
        <div className="bg-slate-800 p-3 rounded-md text-sm font-mono">
          {Object.entries(steps[currentStep].domains).map(([letter, domain], index) => {
            // Check if this domain has changed from previous step
            const prevDomain = prevDomains?.[letter] || []
            const hasChanged =
              prevDomains && (prevDomain.length !== domain.length || !prevDomain.every((val) => domain.includes(val)))

            return (
              <div key={index} className="mb-1 text-white">
                {letter} ={" "}
                {steps[currentStep].mapping[letter] !== undefined && steps[currentStep].mapping[letter] !== null
                  ? steps[currentStep].mapping[letter]
                  : "?"}
                : [
                {domain.map((val, i) => {
                  // Check if this specific value is new or removed
                  const isUpdated =
                    hasChanged &&
                    (steps[currentStep].currentLetter === letter ||
                      !prevDomain.includes(val) ||
                      (prevDomain.includes(val) && steps[currentStep].currentValue === val))

                  return (
                    <span key={i} className={`${isUpdated ? "text-yellow-300 font-bold" : "text-white"}`}>
                      {i > 0 ? ", " : ""}
                      {val}
                    </span>
                  )
                })}
                ]
              </div>
            )
          })}
        </div>
      </div>
    )
  }

  // Function to format the final solution for display
  const formatFinalSolution = (assignments: { [key: string]: number | null }) => {
    return Object.entries(assignments)
        .filter(([_, value]) => value !== null)
        .map(([letter, value]) => `${letter} = ${value}`)
        .join(', ');
  };

  // Function to handle the button click
  const handleSolveButtonClick = () => {
    setIsLoading(true)
    setSteps([])
    setSolution(null)
    setError(null)
    setActiveTab("visualization")
    setCurrentStep(0)
    setDigitToLetters({})
    setEquations([])

    // Build query string for GET request (since EventSource only supports GET)
    const params = buildQuery({
      word1: firstWord,
      word2: secondWord,
      word3: resultWord,
    })
    const es = new EventSource(`http://localhost:5000/solve${params}`)
    setEventSource(es)

    let firstMessage = true
    es.onmessage = (event) => {
      const data = JSON.parse(event.data)
      // First message contains equations
      if (firstMessage && data.equations) {
        setEquations(data.equations)
        firstMessage = false
        return
      }
      firstMessage = false
      if (data.done) {
        setSolution(data.assignments)
        setIsFinished(true)
        // Check if a valid solution exists (all letters assigned to digits)
        const allAssigned = data.assignments && Object.values(data.assignments).every(v => v !== null && v !== undefined)
        setIsSuccess(allAssigned)
        es.close()
        setEventSource(null)
        setIsLoading(false)
      } else {
        setSteps((prev) => {
          const newSteps = [...prev, data];
          setCurrentStep(newSteps.length - 1);
          updateDigitToLetters(data.mapping || {});
          return newSteps;
        });
      }
    }
    es.onerror = (error) => {
      setError("Error contacting backend. Make sure the server is running.")
      es.close()
      setEventSource(null)
      setIsLoading(false)
    }
  }

  // Render all equations and highlight the ones being used
  const renderEquations = () => {
    if (!equations.length) return null
    const currentStepObj = steps[currentStep] || {}
    const usedIndices = currentStepObj.equationsUsed || []
    return (
      <div className="mb-4">
        <h3 className="text-lg font-medium text-white mb-2">Equations:</h3>
        <div className="flex flex-wrap gap-2">
          {equations.map((eq, idx) => (
            <span
              key={idx}
              className={`px-3 py-1 rounded-md font-mono text-sm border transition-all duration-200 ${usedIndices.includes(idx)
                ? "bg-yellow-300 text-slate-900 border-yellow-400 font-bold"
                : "bg-slate-700 text-white border-slate-600"}`}
            >
              {eq}
            </span>
          ))}
        </div>
      </div>
    )
  }

  // Render the progress list with step type, message, and equations used
  const renderProgress = () => (
    <div className="bg-slate-800 p-3 rounded-md h-64 overflow-y-auto font-mono text-sm">
      {steps.slice(0, currentStep + 1).map((step, index) => (
        <div
          key={index}
          className={`mb-2 ${index === currentStep ? "text-yellow-300 font-bold" : "text-gray-300"}`}
        >
          <span className="mr-2">[{step.stepType?.toUpperCase() || "STEP"}]</span>
          {step.message}
          {step.equationsUsed && step.equationsUsed.length > 0 && equations.length > 0 && (
            <span className="ml-2 text-xs text-purple-300">using: {step.equationsUsed.map(i => equations[i]).join(", ")}</span>
          )}
        </div>
      ))}
    </div>
  )

  return (
    <div className="py-8">
      {isClient ? (
        <div className="text-center mb-12">
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-5xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600"
          >
            Cryptarithmetic Visualizer
          </motion.h1>
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: "150px" }}
            transition={{ duration: 1, delay: 0.3 }}
            className="h-1 bg-gradient-to-r from-purple-500 to-pink-500 mx-auto mb-6"
          ></motion.div>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="text-lg text-gray-300"
          >
            Solve cryptarithmetic with visuals
          </motion.p>
        </div>
      ) : (
        <div>Loading...</div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Main content */}
        <div className="lg:col-span-12">
          <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700 overflow-hidden">
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
              <div className="p-4 bg-gradient-to-r from-purple-900 to-slate-900 border-b border-slate-700">
                <TabsList className="grid w-full grid-cols-2 bg-slate-800">
                  <TabsTrigger
                    value="input"
                    className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-600 data-[state=active]:to-pink-600 data-[state=active]:text-white"
                  >
                    Input Puzzle
                  </TabsTrigger>
                  <TabsTrigger
                    value="visualization"
                    className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-600 data-[state=active]:to-pink-600 data-[state=active]:text-white"
                  >
                    Visualization
                  </TabsTrigger>
                </TabsList>
              </div>

              <TabsContent value="input" className="p-6 space-y-6">
                <div className="grid gap-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="firstWord" className="text-gray-300">
                        First Word
                      </Label>
                      <Input
                        id="firstWord"
                        value={firstWord}
                        onChange={(e) => setFirstWord(e.target.value.toUpperCase())}
                        placeholder="SEND"
                        className="font-mono text-lg h-12 bg-slate-700 border-slate-600 text-white"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="secondWord" className="text-gray-300">
                        Second Word
                      </Label>
                      <Input
                        id="secondWord"
                        value={secondWord}
                        onChange={(e) => setSecondWord(e.target.value.toUpperCase())}
                        placeholder="MORE"
                        className="font-mono text-lg h-12 bg-slate-700 border-slate-600 text-white"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="resultWord" className="text-gray-300">
                        Result Word
                      </Label>
                      <Input
                        id="resultWord"
                        value={resultWord}
                        onChange={(e) => setResultWord(e.target.value.toUpperCase())}
                        placeholder="MONEY"
                        className="font-mono text-lg h-12 bg-slate-700 border-slate-600 text-white"
                      />
                    </div>
                  </div>

                  <div className="flex justify-center mt-4">
                    <Button
                      onClick={handleSolveButtonClick}
                      className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white text-lg py-6 px-8"
                    >
                      <Sparkles className="h-5 w-5 mr-2" />
                      Solve Cryptarithmetic
                    </Button>
                  </div>

                  {error && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="bg-red-900/40 border-l-4 border-red-500 text-red-100 p-4 rounded-md"
                    >
                      <div className="flex">
                        <div className="flex-shrink-0">
                          <X className="h-5 w-5 text-red-400" />
                        </div>
                        <div className="ml-3">
                          <p className="text-sm">{error}</p>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  <div className="bg-slate-700/50 p-6 rounded-xl border border-slate-600">
                    <h3 className="text-lg font-medium mb-4 text-white">Examples</h3>
                    <div className="space-y-3">
                      <Button
                        variant="outline"
                        onClick={() => {
                          setFirstWord("SEND")
                          setSecondWord("MORE")
                          setResultWord("MONEY")
                        }}
                        className="bg-slate-800 border-slate-600 hover:bg-slate-700 text-white h-auto py-3 justify-start w-full"
                      >
                        <span className="font-mono font-bold">SEND + MORE = MONEY</span>
                      </Button>

                      <Button
                        variant="outline"
                        onClick={() => {
                          setFirstWord("TWO")
                          setSecondWord("TWO")
                          setResultWord("FOUR")
                        }}
                        className="bg-slate-800 border-slate-600 hover:bg-slate-700 text-white h-auto py-3 justify-start w-full"
                      >
                        <span className="font-mono font-bold">TWO + TWO = FOUR</span>
                      </Button>

                      <Button
                        variant="outline"
                        onClick={() => {
                          setFirstWord("BASE")
                          setSecondWord("BALL")
                          setResultWord("GAMES")
                        }}
                        className="bg-slate-800 border-slate-600 hover:bg-slate-700 text-white h-auto py-3 justify-start w-full"
                      >
                        <span className="font-mono font-bold">BASE + BALL = GAMES</span>
                      </Button>

                      <Button
                        variant="outline"
                        onClick={() => {
                          setFirstWord("CROSS")
                          setSecondWord("ROADS")
                          setResultWord("DANGER")
                        }}
                        className="bg-slate-800 border-slate-600 hover:bg-slate-700 text-white h-auto py-3 justify-start w-full"
                      >
                        <span className="font-mono font-bold">CROSS + ROADS = DANGER</span>
                      </Button>

                      <Button
                        variant="outline"
                        onClick={() => {
                          setFirstWord("SATURN")
                          setSecondWord("URANUS")
                          setResultWord("PLANETS")
                        }}
                        className="bg-slate-800 border-slate-600 hover:bg-slate-700 text-white h-auto py-3 justify-start w-full"
                      >
                        <span className="font-mono font-bold">SATURN + URANUS = PLANETS</span>
                      </Button>

                      <Button
                        variant="outline"
                        onClick={() => {
                          setFirstWord("FORTY")
                          setSecondWord("TEN")
                          setResultWord("FIFTY")
                        }}
                        className="bg-slate-800 border-slate-600 hover:bg-slate-700 text-white h-auto py-3 justify-start w-full"
                      >
                        <span className="font-mono font-bold">FORTY + TEN = FIFTY</span>
                      </Button>
                    </div>
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="visualization">
                {isFinished && (
                  <div className={`mb-4 p-4 rounded-lg text-lg font-bold text-center border-2 ${isSuccess ? 'bg-green-700/80 border-green-400 text-white' : 'bg-red-700/80 border-red-400 text-white'}`}>
                    {isSuccess ? (
                      <>
                        ✅ Solution Found!<br />
                        <span className="font-mono text-base font-normal">{formatFinalSolution(solution || {})}</span>
                      </>
                    ) : (
                      <>❌ No Solution Found.</>
                    )}
                  </div>
                )}
                {steps.length > 0 ? (
                  <div className="p-6">
                    {/* Render all equations at the top */}
                    {renderEquations()}
                    <div className="bg-slate-700/50 p-4 rounded-xl border border-slate-600 mb-4">
                      <h3 className="text-xl font-medium mb-2 text-center text-white">
                        {firstWord} + {secondWord} = {resultWord}
                      </h3>
                      <div className="flex flex-wrap gap-2 justify-center mb-4">
                        {uniqueLetters.map((letter) => (
                          <Badge key={letter} className="bg-slate-600 text-white">
                            {letter}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      {/* Progress section */}
                      <div className="bg-slate-700/50 p-4 rounded-xl border border-slate-600">
                        <h3 className="text-lg font-medium mb-2 text-white">Progress</h3>
                        {renderProgress()}

                        {/* Controls */}
                        <div className="mt-4 space-y-4">
                          <div className="flex items-center justify-between">
                            <span className="text-sm text-gray-300">Speed</span>
                            <Badge variant="outline" className="bg-slate-700 text-gray-300 border-slate-600">
                              {speed}%
                            </Badge>
                          </div>
                          <Slider
                            value={[speed]}
                            min={1}
                            max={100}
                            step={1}
                            onValueChange={(value) => setSpeed(value[0])}
                          />

                          <div className="grid grid-cols-3 gap-2">
                            <Button
                              variant="outline"
                              onClick={resetVisualization}
                              className="bg-slate-700 border-slate-600 hover:bg-slate-600 text-white"
                            >
                              <RotateCcw className="h-4 w-4 mr-2" />
                              Reset
                            </Button>
                            <Button
                              onClick={toggleVisualization}
                              disabled={currentStep >= steps.length - 1}
                              className={`${
                                isRunning
                                  ? "bg-amber-600 hover:bg-amber-700"
                                  : "bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
                              } text-white`}
                            >
                              {isRunning ? (
                                <>
                                  <Pause className="h-4 w-4 mr-2" />
                                  Pause
                                </>
                              ) : (
                                <>
                                  <Play className="h-4 w-4 mr-2" />
                                  {currentStep === 0 ? "Start" : "Resume"}
                                </>
                              )}
                            </Button>
                            <Button
                              onClick={nextStep}
                              disabled={currentStep >= steps.length - 1}
                              className="bg-slate-700 border-slate-600 hover:bg-slate-600 text-white"
                            >
                              <SkipForward className="h-4 w-4 mr-2" />
                              Next
                            </Button>
                          </div>
                        </div>

                        {renderDomains()}
                      </div>

                      {/* Decision Tree section */}
                      <div className="bg-slate-700/50 p-4 rounded-xl border border-slate-600">
                        <h3 className="text-lg font-medium mb-2 text-white">Decision Tree</h3>
                        <div className="bg-slate-800 p-3 rounded-md h-[500px] overflow-y-auto flex justify-center">
                          {renderDecisionTree()}
                        </div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-16">
                    <div className="inline-block p-6 bg-slate-700 rounded-full mb-4">
                      <Calculator className="h-12 w-12 text-purple-400" />
                    </div>
                    <p className="text-gray-300 mb-4 text-lg">
                      No visualization available. Please solve a puzzle first.
                    </p>
                    <Button
                      onClick={() => setActiveTab("input")}
                      className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white"
                    >
                      Go to Input
                    </Button>
                  </div>
                )}
              </TabsContent>
            </Tabs>
          </Card>
        </div>
      </div>

      {/* Floating math symbols for decoration */}
      <ClientOnly>
        <div className="fixed inset-0 pointer-events-none overflow-hidden">
          {Array.from({ length: 30 }).map((_, i) => (
            <div
              key={i}
              className="absolute text-white text-opacity-5 font-mono"
              style={{
                top: `${Math.random() * 100}%`,
                left: `${Math.random() * 100}%`,
                fontSize: `${Math.random() * 40 + 20}px`,
                transform: `rotate(${Math.random() * 360}deg)`,
                opacity: Math.random() * 0.2 + 0.1,
              }}
            >
              {
                ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "=", "×", "÷", "−", "√"][
                  Math.floor(Math.random() * 16)
                ]
              }
            </div>
          ))}
        </div>
      </ClientOnly>
    </div>
  )
}
