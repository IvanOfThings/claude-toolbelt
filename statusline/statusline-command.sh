#!/bin/bash
# Claude Code status line script

input=$(cat)

model=$(echo "$input" | jq -r '.model.display_name // "Unknown Model"')

# --- Account usage % (context window used percentage as proxy) ---
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')

if [ -n "$used_pct" ]; then
  used_pct_int=$(printf "%.0f" "$used_pct" 2>/dev/null || echo 0)
  usage_display="Usage: ${used_pct_int}%"
else
  usage_display="Usage: 0%"
fi

# --- Hours until token reset ---
# Claude Pro/Max resets on a 5-hour rolling window.
# Calculate seconds elapsed in the current 5-hour block, then time remaining.
now_epoch=$(date +%s)
block_seconds=$(( 5 * 3600 ))
elapsed_in_block=$(( now_epoch % block_seconds ))
remaining_seconds=$(( block_seconds - elapsed_in_block ))
remaining_hours=$(( remaining_seconds / 3600 ))
remaining_minutes=$(( (remaining_seconds % 3600) / 60 ))
reset_display="Reset in: ${remaining_hours}h ${remaining_minutes}m"

printf "%s  |  %s  |  %s" \
  "$model" \
  "$usage_display" \
  "$reset_display"
