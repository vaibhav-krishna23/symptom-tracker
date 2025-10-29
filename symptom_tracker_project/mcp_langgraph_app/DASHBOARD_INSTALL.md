# 📊 Dashboard Feature - Installation & Setup

## Quick Install

### 1. Update Dependencies

```bash
cd symptom_tracker_project/mcp_langgraph_app
pip install pandas
```

Or reinstall all dependencies:

```bash
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python -c "import pandas; print('Pandas version:', pandas.__version__)"
```

Expected output: `Pandas version: 2.x.x`

### 3. Restart Application

**Terminal 1 - Backend:**
```bash
cd symptom_tracker_project/mcp_langgraph_app
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd symptom_tracker_project/mcp_langgraph_app
streamlit run streamlit_app/app_v2.py
```

### 4. Access Dashboard

1. Open browser: http://localhost:8501
2. Login to your account
3. Click **"📊 Dashboard"** in sidebar
4. Enjoy your new insights!

## What's Included

### Modified Files:
- ✅ `api/main.py` - New insights endpoint
- ✅ `streamlit_app/app_v2.py` - Enhanced dashboard UI
- ✅ `requirements.txt` - Added pandas
- ✅ `README.md` - Updated documentation
- ✅ `CHANGELOG.md` - Version 2.0.1 entry

### New Files:
- ✅ `DASHBOARD_FEATURE.md` - Technical docs
- ✅ `DASHBOARD_USER_GUIDE.md` - User guide
- ✅ `DASHBOARD_SUMMARY.md` - Quick summary
- ✅ `DASHBOARD_INSTALL.md` - This file

## Testing the Dashboard

### 1. Check API Endpoint

```bash
# Get your auth token first (login via UI or API)
TOKEN="your_jwt_token_here"

# Test insights endpoint
curl -X GET http://localhost:8000/api/v1/dashboard/insights \
  -H "Authorization: Bearer $TOKEN"
```

Expected response:
```json
{
  "total_sessions": 5,
  "total_symptoms": 15,
  "avg_severity": 5.2,
  "red_flag_count": 1,
  "symptom_frequency": {...},
  "severity_trend": [...],
  "recent_sessions": [...],
  "appointments_count": 2,
  "avg_intensity_by_symptom": {...}
}
```

### 2. Test Dashboard UI

1. Login to application
2. Navigate to Dashboard
3. Verify you see:
   - ✅ 5 metric cards at top
   - ✅ Severity trend line chart
   - ✅ Two bar charts (symptoms & intensity)
   - ✅ Recent sessions list
   - ✅ Health insights section

### 3. Test Session Details

1. Click any session in "Recent Sessions"
2. Click "📄 View Full Details"
3. Verify you see:
   - ✅ Session overview metrics
   - ✅ AI analysis box
   - ✅ Color-coded symptom cards
   - ✅ Conversation history
   - ✅ Back button

## Troubleshooting

### Issue: "No module named 'pandas'"

**Solution:**
```bash
pip install pandas
```

### Issue: Charts not displaying

**Solution:**
1. Check browser console for errors
2. Verify pandas is installed: `pip list | grep pandas`
3. Restart Streamlit: `Ctrl+C` then rerun

### Issue: "No symptom logs yet"

**Solution:**
1. Log some symptoms first via "🌡️ Log Symptoms"
2. Return to dashboard
3. Data should now appear

### Issue: API returns empty data

**Solution:**
1. Verify you're logged in (check token)
2. Ensure you have logged symptoms
3. Check database connection
4. Review backend logs for errors

### Issue: Session details not loading

**Solution:**
1. Verify session_id is valid
2. Check that session belongs to logged-in user
3. Review API logs: `GET /api/v1/dashboard/session/{id}/details`

## Database Requirements

No database changes needed! The dashboard uses existing tables:
- ✅ `sessions` - Already exists
- ✅ `symptom_entries` - Already exists
- ✅ `appointments` - Already exists
- ✅ `patients` - Already exists

## Performance Notes

### Data Volume
- Dashboard loads efficiently with 100+ sessions
- Charts display last 10 sessions for clarity
- Top 10 symptoms shown in frequency chart
- Top 5 symptoms in intensity chart

### Optimization
- Database queries use indexes
- Aggregations done in Python (not DB)
- Charts rendered client-side by Streamlit
- No additional caching needed

## Browser Compatibility

Tested and working on:
- ✅ Chrome 120+
- ✅ Firefox 120+
- ✅ Edge 120+
- ✅ Safari 17+

## Mobile Support

Dashboard is responsive and works on:
- ✅ Desktop (1920x1080+)
- ✅ Laptop (1366x768+)
- ✅ Tablet (768x1024+)
- ⚠️ Mobile (limited, best on tablet+)

## Upgrade Path

### From v2.0.0 to v2.0.1

**No breaking changes!** Simply:
1. Pull latest code
2. Install pandas: `pip install pandas`
3. Restart application
4. Dashboard automatically available

### Backward Compatibility

- ✅ All v2.0.0 features still work
- ✅ Existing data fully compatible
- ✅ No database migrations needed
- ✅ API v1 endpoints unchanged

## Next Steps

1. **Read User Guide**: See `DASHBOARD_USER_GUIDE.md`
2. **Explore Features**: Try all dashboard sections
3. **Log More Symptoms**: More data = better insights
4. **Share Feedback**: Report issues or suggestions

## Support

### Documentation
- **Technical**: `DASHBOARD_FEATURE.md`
- **User Guide**: `DASHBOARD_USER_GUIDE.md`
- **Summary**: `DASHBOARD_SUMMARY.md`
- **Main README**: `README.md`

### API Documentation
- Interactive docs: http://localhost:8000/docs
- Insights endpoint: `/api/v1/dashboard/insights`
- Session details: `/api/v1/dashboard/session/{id}/details`

### Troubleshooting
1. Check terminal logs (backend & frontend)
2. Review browser console (F12)
3. Verify all dependencies installed
4. Ensure database is accessible

## Version Info

- **Feature Version**: 2.0.1
- **Release Date**: 2024
- **Status**: ✅ Production Ready
- **Dependencies**: pandas (new)

---

**Congratulations!** 🎉 Your enhanced dashboard is ready to use!

Start tracking your health with beautiful visualizations and AI-powered insights.
