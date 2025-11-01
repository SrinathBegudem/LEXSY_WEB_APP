# Infinite Loop Fix - Doc Assistant

## Problem Description

The Doc Assistant was experiencing an infinite loop where:
1. AI asks for "Investor Name" (Field 2)
2. User provides "JISOOOO BP"
3. AI responds with an error and asks for "Investor Name" again
4. Loop continues indefinitely

### Root Cause

The issue was in `/backend/services/ai_service.py` in the `process_message()` method (line 276):

```python
# OLD CODE (BUGGY):
actual_index = len(filled_values)  # ❌ WRONG
```

**Why this caused the loop:**
- Frontend/AI displays "Field 2 of 11: Investor Name"
- User enters "JISOOOO BP" 
- Backend receives `current_index=0` (because no fields filled yet)
- Backend **recalculates** index as `len(filled_values) = 0`
- Backend tries to validate "JISOOOO BP" against Field 0 (Company Name) ❌
- Validation fails (name doesn't match company format)
- AI asks for Field 0 again, but frontend still shows Field 2
- **Mismatch between what AI asks and what backend validates**

## Solution

Fixed the logic to use the `current_index` parameter directly:

```python
# NEW CODE (FIXED):
actual_index = current_index  # ✅ CORRECT

# Plus safety check to skip already-filled fields
while actual_index < len(placeholders):
    ph = placeholders[actual_index]
    ph_id = ph.get('id', ph['key'])
    ph_key = ph.get('key')
    
    is_filled = (ph_id in filled_values or ph_key in filled_values)
    
    if not is_filled:
        break
    
    actual_index += 1
```

### Why this works:
- `current_index` parameter represents which field we're **currently asking about**
- This stays synchronized between frontend (what user sees) and backend (what gets validated)
- The safety loop handles edge cases where auto-fills might have filled the current field

## Files Changed

1. **`/backend/services/ai_service.py`** (lines 275-297)
   - Fixed `process_message()` method to use `current_index` parameter
   - Added safety loop to skip already-filled fields
   - Updated docstring to clarify `current_index` meaning

## Testing Steps

### Manual Test (using the exact scenario from Probs.txt):

1. **Start backend**:
   ```bash
   cd backend
   python app.py
   ```

2. **Start frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Upload a SAFE Agreement template** (or any document with multiple fields)

4. **Test the scenario from Probs.txt**:
   - Field 1 (Company Name): Enter any company name → Should proceed to Field 2
   - Field 2 (Investor Name): Enter "JISOOOO BP" → **Should accept and proceed to Field 3**
   - Field 3 (Purchase Amount): Enter "10000" → **Should accept and proceed to Field 4**
   - Continue filling fields → **Should NOT loop back to previous fields**

### Expected Behavior (After Fix):
- ✅ Each field is asked only once
- ✅ User's response is validated against the correct field
- ✅ Progress moves forward after valid input
- ✅ No infinite loops asking for the same field

### Before Fix Behavior:
- ❌ Field 2 asked → User answers → AI asks Field 2 again (loop)
- ❌ Validation errors for wrong field types
- ❌ Progress stuck at 0/11 fields

## Technical Details

### Key Insight from Old Working Version

The old version in Probs.txt (lines 401-418) had the correct logic:
```python
response = ai_service.process_message(
    user_message=user_message,
    placeholders=placeholders,
    filled_values=filled_values,
    current_index=current_index,  # ← Passed current index
    ai_context=ai_context
)

if response.get('placeholder_filled'):
    # ... update filled_values ...
    session_data['current_placeholder_index'] = current_index + 1  # ← Increment
```

The new version now follows this same pattern:
1. `app.py` maintains `current_placeholder_index` in session
2. Passes it to `ai_service.process_message()`
3. `ai_service` uses it to validate the **current field** (not recalculated)
4. Returns `next_index` for the next unfilled field
5. `app.py` updates `current_placeholder_index` based on response

## Verification

✅ **Syntax Check**: Passed (`python -m py_compile services/ai_service.py`)  
✅ **Linter**: No errors  
✅ **Logic**: Matches working pattern from old version  

## Notes

- The fix maintains backward compatibility
- Auto-fill logic for duplicate fields still works correctly
- Edge cases (edited fields, out-of-order filling) are handled by the safety loop

