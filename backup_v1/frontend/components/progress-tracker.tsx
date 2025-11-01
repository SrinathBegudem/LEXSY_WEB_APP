'use client';

import { CheckCircle2, Circle, ChevronDown } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { cn } from '@/lib/utils';
import type { Placeholder } from '@/lib/types';
import { useState, useMemo } from 'react';

interface ProgressTrackerProps {
  placeholders: Placeholder[];
  filledValues: Record<string, string>;
  currentIndex: number;
  progress: number;
}

export function ProgressTracker({
  placeholders,
  filledValues,
  currentIndex,
  progress,
}: ProgressTrackerProps) {
  const completedCount = Object.keys(filledValues).length;
  const totalCount = placeholders.length;
  const [expandedGroups, setExpandedGroups] = useState<Record<number, boolean>>({
    0: true,
  });

  // Group placeholders into sections
  const groupedPlaceholders = useMemo(() => {
    const itemsPerGroup = Math.max(1, Math.ceil(totalCount / 5));
    const groups = [];
    for (let i = 0; i < placeholders.length; i += itemsPerGroup) {
      groups.push(placeholders.slice(i, i + itemsPerGroup));
    }
    return groups;
  }, [placeholders, totalCount]);

  const toggleGroup = (groupIdx: number) => {
    setExpandedGroups((prev) => ({
      ...prev,
      [groupIdx]: !prev[groupIdx],
    }));
  };

  return (
    <div className="flex flex-col">
      {/* Header - Compact */}
      <div className="p-4 border-b border-slate-200/50 bg-gradient-to-r from-white to-slate-50/50 backdrop-blur-sm">
        <div className="space-y-3">
          <h2 className="text-sm font-bold text-slate-900">Progress Tracker</h2>
          
          {/* Main Progress Bar - Compact */}
          <div>
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-medium text-slate-700">Overall Completion</span>
              <span className="text-sm font-bold text-primary transition-all duration-500">{progress.toFixed(0)}%</span>
            </div>
            <div className="relative h-1.5 bg-slate-200/50 rounded-full overflow-hidden backdrop-blur-sm">
              <div
                className="absolute inset-y-0 left-0 bg-gradient-to-r from-primary to-primary/70 rounded-full transition-all duration-500 ease-out shadow-md"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          {/* Stats - Compact */}
          <div className="grid grid-cols-2 gap-2">
            <div className="bg-gradient-to-br from-primary/10 to-primary/5 rounded-lg p-2 text-center border border-primary/10 hover:border-primary/20 transition-all duration-300 hover:shadow-sm">
              <div className="text-lg font-bold text-primary transition-all duration-500">{completedCount}</div>
              <div className="text-xs font-medium text-slate-600">Completed</div>
            </div>
            <div className="bg-gradient-to-br from-slate-100/50 to-slate-50 rounded-lg p-2 text-center border border-slate-200/50 hover:border-slate-200 transition-all duration-300 hover:shadow-sm">
              <div className="text-lg font-bold text-slate-700 transition-all duration-500">{totalCount - completedCount}</div>
              <div className="text-xs font-medium text-slate-600">Remaining</div>
            </div>
          </div>
        </div>
      </div>

      {/* Fields List - Compact, limited height */}
      <div className="max-h-96 overflow-y-auto scrollbar-hide">
        <div className="divide-y divide-slate-100/50">
          {groupedPlaceholders.map((group, groupIdx) => {
            const groupStartIdx = groupIdx * Math.ceil(totalCount / 5);
            const isExpanded = expandedGroups[groupIdx];
            const groupCompleted = group.filter((p) => {
              const id = p.id || p.key;
              return id in filledValues;
            }).length;
                
                return (
              <div key={groupIdx} className="border-b border-slate-100/50 transition-all duration-300">
                {/* Group Header - Better Visual */}
                <button
                  onClick={() => toggleGroup(groupIdx)}
                  className="w-full px-5 py-3 flex items-center gap-3 hover:bg-slate-50/50 active:bg-slate-100/50 transition-all duration-200 text-left group"
                >
                  <ChevronDown
                    className={cn(
                      'h-5 w-5 text-slate-400 transition-transform duration-300 flex-shrink-0 group-hover:text-slate-600',
                      isExpanded && 'rotate-180'
                    )}
                  />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-bold text-slate-800">
                      Section {groupIdx + 1}
                    </div>
                    <div className="text-xs text-slate-500 mt-0.5">
                      {groupCompleted} / {group.length} fields completed
                    </div>
                  </div>
                  <div className="w-14 h-1 bg-slate-200/50 rounded-full overflow-hidden flex-shrink-0">
                    <div
                      className="h-full bg-gradient-to-r from-primary to-primary/70 transition-all duration-300 shadow-sm"
                      style={{
                        width: `${(groupCompleted / group.length) * 100}%`,
                      }}
                    />
                  </div>
                </button>

                {/* Group Items - Better spacing */}
                {isExpanded && (
                  <div className="space-y-1 px-2 py-2 bg-slate-50/30 backdrop-blur-sm transition-all duration-300">
                    {group.map((placeholder, itemIdx) => {
                      const absoluteIdx = groupStartIdx + itemIdx;
                      const id = placeholder.id || placeholder.key;
                      const isFilled = id in filledValues;
                      const isCurrent = absoluteIdx === currentIndex;

                      return (
                        <div
                          key={id}
                          className={cn(
                            'px-3 py-2.5 rounded-lg transition-all duration-200 group hover:shadow-sm',
                            isCurrent &&
                              'bg-primary/15 border-l-3 border-primary shadow-sm scale-[1.02]',
                            isFilled && !isCurrent && 'opacity-50 hover:opacity-75',
                            !isCurrent && !isFilled && 'hover:bg-white'
                          )}
                        >
                          <div className="flex items-center gap-2.5 min-w-0">
                    {isFilled ? (
                              <CheckCircle2 className="h-4 w-4 text-green-500 flex-shrink-0 transition-transform duration-300 group-hover:scale-110" />
                    ) : (
                              <Circle className="h-4 w-4 text-slate-300 flex-shrink-0 transition-all duration-300 group-hover:text-slate-400" />
                    )}
                            <div className="min-w-0 flex-1">
                              <div
                      className={cn(
                                  'text-sm leading-tight truncate transition-all duration-300',
                                  isCurrent && 'font-bold text-primary',
                                  isFilled &&
                                    'text-slate-500 line-through',
                                  !isFilled &&
                                    !isCurrent &&
                                    'text-slate-700 font-medium'
                      )}
                    >
                      {placeholder.name}
                              </div>
                            </div>
                    {isCurrent && (
                              <Badge
                                variant="default"
                                className="text-xs py-0.5 px-2 flex-shrink-0 font-semibold animate-pulse"
                              >
                                Now
                      </Badge>
                    )}
                          </div>
                  </div>
                );
              })}
                  </div>
              )}
            </div>
            );
          })}
        </div>
      </div>

      {/* Footer Stats - Compact */}
      <div className="border-t border-slate-200/50 bg-gradient-to-t from-slate-50/50 to-white backdrop-blur-sm p-3 transition-all duration-300">
        <div className="text-center">
          <div className="font-bold text-slate-900 text-xs transition-all duration-300">
            {completedCount === totalCount ? '✨ Complete!' : `${totalCount - completedCount} fields left`}
          </div>
          <div className="text-xs text-slate-500 transition-all duration-300">
            {completedCount === totalCount
              ? 'Ready to download'
              : `${Math.round((completedCount / totalCount) * 100)}% progress`}
          </div>
        </div>
      </div>
    </div>
  );
}

