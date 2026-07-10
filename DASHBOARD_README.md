# Dashboard Web App

A modern, responsive dashboard application with interactive charts, task management, and analytics.

## Features

✨ **Overview Section**
- Real-time metric cards (Sales, Users, Revenue, Engagement)
- Interactive sales trend chart
- Traffic sources visualization
- Recent activity table with search

📊 **Analytics Section**
- Monthly growth bar chart
- User distribution radar chart
- Performance metrics with progress bars

✓ **Task Management**
- Add/delete tasks
- Mark tasks as complete
- Real-time task updates

⚙️ **Settings**
- Notification preferences
- Privacy controls
- Theme selection

## Quick Start

1. **Open the dashboard**
   - Open `dashboard.html` in your web browser
   - No installation or build process required

2. **Navigate sections**
   - Use the sidebar to switch between Overview, Analytics, Tasks, and Settings
   - Use keyboard shortcuts:
     - `Ctrl+K` or `Cmd+K` - Focus search box
     - `Ctrl+D` or `Cmd+D` - Toggle dark/light theme

3. **Add tasks**
   - Go to Tasks section
   - Type task name and click "Add Task" or press Enter
   - Check off completed tasks
   - Delete tasks with the ✕ button

4. **Search**
   - Use the search box to filter recent activity
   - Works in real-time as you type

## Files

- `dashboard.html` - Main HTML structure
- `dashboard.css` - Styling and responsive design
- `dashboard.js` - Interactive functionality and charts

## Browser Compatibility

✅ Chrome/Edge (Latest)
✅ Firefox (Latest)
✅ Safari (Latest)
✅ Mobile browsers

## Technologies

- **Chart.js 3.9.1** - Data visualization
- **Vanilla JavaScript** - No dependencies
- **CSS3** - Modern styling with gradients

## Features Included

### Charts
- Line chart (Sales trends)
- Doughnut chart (Traffic sources)
- Bar chart (Monthly growth)
- Radar chart (User distribution)

### Functionality
- Real-time metric updates
- Search and filter
- Task CRUD operations
- Data export (JSON/CSV)
- Theme toggle
- Keyboard shortcuts
- Notifications system
- Error handling

## Customization

### Change Colors
Edit `dashboard.css` to customize:
```css
.sidebar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Update Chart Data
Edit `dashboard.js` in the `initializeCharts()` function:
```javascript
data: [12000, 19000, 15000, 25000, 22000, 30000]
```

### Add New Metrics
1. Add HTML in `dashboard.html`
2. Style in `dashboard.css`
3. Add JavaScript logic in `dashboard.js`

## Troubleshooting

**Charts not showing?**
- Ensure Chart.js library is loaded
- Check browser console for errors
- Verify canvas elements have IDs

**Tasks not working?**
- Check that taskInput and tasksList elements exist
- Verify JavaScript is enabled
- Clear browser cache and reload

**Search not filtering?**
- Ensure activity table exists
- Check table structure (tbody required)
- Try searching for different keywords

## Performance

- Lightweight: No heavy dependencies
- Fast loading: < 1MB total size
- Responsive: Works on all devices
- Accessible: Keyboard navigation support

## Browser Console

Open browser console (F12) to see:
- Chart initialization status
- Task operations
- Search activity
- Any errors or warnings

## Future Enhancements

- [ ] Dark theme styling
- [ ] Export to PDF
- [ ] Data persistence with localStorage
- [ ] API integration
- [ ] Multi-user support
- [ ] Real-time data updates

## License

Open source - Feel free to use and modify

## Support

For issues or questions:
1. Check browser console (F12)
2. Verify all files are in same directory
3. Try different browser
4. Clear cache and reload
