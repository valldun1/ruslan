import { useQuery } from '@tanstack/react-query'

import { getRuslanConfigRecord } from '@/ruslan'
import { queryClient, writeCache } from '@/lib/query-client'
import type { RuslanConfigRecord } from '@/types/ruslan'

// One shared cache for the whole profile config record (`GET /api/config`).
// Every settings surface (MCP, model, config) reads and writes through this key
// so a save in one shows in the others, and revisiting a tab paints the cache
// instead of blanking on a fresh fetch.
//
// Distinct from session/hooks/use-ruslan-config.ts, which is side-effecting —
// it pushes personality/cwd/voice/… into the session stores for live chat.
export const RUSLAN_CONFIG_KEY = ['ruslan-config-record'] as const

// staleTime 0 → serve cache instantly, background-revalidate on every mount.
export const useRuslanConfigRecord = () =>
  useQuery({ queryKey: RUSLAN_CONFIG_KEY, queryFn: getRuslanConfigRecord, staleTime: 0 })

export const setRuslanConfigCache = writeCache<RuslanConfigRecord>(RUSLAN_CONFIG_KEY)

export const invalidateRuslanConfig = () => queryClient.invalidateQueries({ queryKey: RUSLAN_CONFIG_KEY })
