# Travel Planner (single Jupyter cell)
import random, datetime, os, urllib.parse
from IPython.display import display, HTML
try:
    import ipywidgets as widgets
    HAS_WIDGETS = True
except Exception:
    HAS_WIDGETS = False

# -------------------------
# 1) Built-in sample POI data (example cities)
# -------------------------
ATTRACTIONS = {
    "Paris": [
        {"name":"Eiffel Tower","category":"landmark","hours":2,"cost":30,"note":"Iconic view; book tickets early."},
        {"name":"Louvre Museum","category":"culture","hours":3,"cost":17,"note":"World-class art collection."},
        {"name":"Musée d'Orsay","category":"culture","hours":2.5,"cost":16,"note":"Impressionist masterpieces."},
        {"name":"Montmartre & Sacré-Cœur","category":"culture","hours":2.5,"cost":0,"note":"Bohemian hilltop neighborhood."},
        {"name":"Seine River Cruise","category":"relax","hours":1.5,"cost":15,"note":"Great for evening views."},
        {"name":"Le Marais (food & shopping)","category":"food","hours":2,"cost":20,"note":"Boutiques & cafes."},
        {"name":"Versailles (day trip)","category":"culture","hours":6,"cost":25,"note":"Palace + gardens; allow a full day."}
    ],
    "New York": [
        {"name":"Central Park","category":"nature","hours":2.5,"cost":0,"note":"Relax, walk or bike."},
        {"name":"Metropolitan Museum of Art (The Met)","category":"culture","hours":3,"cost":25,"note":"Large museum; pick highlights."},
        {"name":"Times Square","category":"landmark","hours":1.5,"cost":0,"note":"Busy, vibrant at night."},
        {"name":"Statue of Liberty (ferry)","category":"landmark","hours":3.5,"cost":25,"note":"Reserve ferry time."},
        {"name":"Brooklyn Bridge & DUMBO","category":"landmark","hours":2,"cost":0,"note":"Great skyline views."},
        {"name":"9/11 Memorial & Museum","category":"culture","hours":2,"cost":26,"note":"Powerful memorial."}
    ],
    "Tokyo": [
        {"name":"Senso-ji Temple (Asakusa)","category":"culture","hours":1.5,"cost":0,"note":"Historic temple and market street."},
        {"name":"Meiji Shrine & Harajuku","category":"culture","hours":2,"cost":0,"note":"Shrine plus trendy neighborhood."},
        {"name":"Shibuya Crossing & Center Gai","category":"landmark","hours":1.5,"cost":0,"note":"Iconic intersection and shopping."},
        {"name":"Tokyo Skytree","category":"landmark","hours":2,"cost":20,"note":"Observation decks."},
        {"name":"Tsukiji Outer Market","category":"food","hours":1.5,"cost":20,"note":"Seafood stalls and snacks."},
        {"name":"Ueno Park & Museums","category":"culture","hours":2.5,"cost":10,"note":"Museums and park space."}
    ],
    "Mumbai": [
        {"name":"Gateway of India","category":"landmark","hours":1,"cost":0,"note":"Historic waterfront monument."},
        {"name":"Elephanta Caves (ferry)","category":"culture","hours":4,"cost":10,"note":"Day trip by ferry."},
        {"name":"Marine Drive & Chowpatty","category":"relax","hours":1.5,"cost":0,"note":"Sunset strolls."},
        {"name":"Chhatrapati Shivaji Maharaj Vastu Sangrahalaya","category":"culture","hours":2,"cost":5,"note":"Museum with diverse collection."},
        {"name":"Colaba Causeway (markets)","category":"shopping","hours":2,"cost":15,"note":"Street shopping & cafes."},
        {"name":"Sanjay Gandhi National Park","category":"nature","hours":4,"cost":8,"note":"Nature and small hikes."}
    ]
}

# -------------------------
# Helpers: itinerary generation & HTML
# -------------------------
def find_matching_attractions(city, interests, budget_level):
    pool = ATTRACTIONS.get(city, [])
    if not interests:
        filtered = pool[:]
    else:
        # allow category match (interest like 'culture','food','nature','shopping','landmark','relax')
        filtered = [p for p in pool if p["category"] in interests]
    # budget_level: 'low','medium','high' — filter by cost heuristics
    if budget_level == "low":
        filtered = [p for p in filtered if p["cost"] <= 15]
    elif budget_level == "medium":
        filtered = [p for p in filtered if p["cost"] <= 30]
    # else high: keep all
    if not filtered:
        filtered = pool[:]  # fallback to everything
    random.shuffle(filtered)
    return filtered

def generate_itinerary(city, start_date, days, interests, budget_level, activities_per_day=3):
    pool = find_matching_attractions(city, interests, budget_level)
    used = set()
    itinerary = []
    # approximate day windows in hours to place activities
    day_windows = [("Morning",9,12), ("Afternoon",13,17), ("Evening",18,21)]
    for d in range(days):
        day_date = start_date + datetime.timedelta(days=d)
        day_plan = {"date": day_date, "slots": []}
        # pick up to activities_per_day activities spaced into windows
        choices = [p for p in pool if p["name"] not in used]
        idx = 0
        for slot_name, start_h, end_h in day_windows:
            if len(day_plan["slots"]) >= activities_per_day:
                break
            if idx >= len(choices):
                break
            # select an attraction that fits a single slot (duration <= slot hours + small buffer)
            candidate = choices[idx]
            idx += 1
            used.add(candidate["name"])
            est_start = start_h
            est_end = min(end_h, start_h + max(1, int(candidate["hours"])))
            slot = {
                "time_window": slot_name,
                "start_hour": est_start,
                "end_hour": est_end,
                "name": candidate["name"],
                "category": candidate["category"],
                "hours": candidate["hours"],
                "cost": candidate["cost"],
                "note": candidate.get("note","")
            }
            day_plan["slots"].append(slot)
        itinerary.append(day_plan)
    return itinerary

def maps_link(for_name, city):
    q = urllib.parse.quote_plus(f"{for_name} {city}")
    return f"https://www.google.com/maps/search/{q}"

def itinerary_to_html(city, start_date, days, itinerary, interests, budget_level):
    html = f"<div style='font-family:Arial; max-width:880px;'>"
    html += f"<h2 style='color:#1f77b4;'>Trip plan — {city} ({start_date.isoformat()} for {days} day(s))</h2>"
    html += f"<p><b>Interests:</b> {', '.join(interests) if interests else 'All'} • <b>Budget:</b> {budget_level.title()}</p>"
    for day in itinerary:
        html += f"<div style='background:#f7fbff;padding:12px;border-radius:8px;margin-bottom:10px;'>"
        html += f"<h3 style='margin:4px 0;'>{day['date'].strftime('%A, %b %d')}</h3>"
        if not day["slots"]:
            html += "<p style='color:#666;'>No activities scheduled for this day.</p>"
        else:
            html += "<ol>"
            for s in day["slots"]:
                link = maps_link(s["name"], city)
                html += ("<li style='margin-bottom:6px;'><b>{name}</b> "
                         f"(<i>{s['category']}</i>) — approx {s['hours']} h — "
                         f"est {s['start_hour']}:00–{s['end_hour']}:00 — ${s['cost']}<br>"
                         f"<span style='color:#333'>{s['note']}</span> "
                         f"<a href='{link}' target='_blank'>[map]</a></li>").format(name=s["name"])
            html += "</ol>"
        html += "</div>"
    # packing tips
    html += "<div style='padding:12px;border-radius:8px;background:#fff7e6;margin-top:8px;'>"
    html += "<h4>Packing & Travel tips</h4><ul>"
    html += "<li>Carry a comfortable pair of shoes and a small day bag.</li>"
    html += "<li>Keep a printed/phone copy of tickets and ID.</li>"
    html += "<li>For city trips, carry a portable charger and a water bottle.</li>"
    html += "</ul></div>"
    # cost summary
    total_cost = sum(s["cost"] for day in itinerary for s in day["slots"])
    html += f"<div style='margin-top:8px;padding:10px;border-radius:8px;background:#eef7ee;'><b>Estimated activity cost:</b> ${total_cost} (approx)</div>"
    html += "</div>"
    return html

# -------------------------
# UI: ipywidgets version (or fallback)
# -------------------------
def run_with_widgets():
    city_dd = widgets.Dropdown(options=sorted(ATTRACTIONS.keys()), description="Destination:", style={'description_width':'initial'})
    start_picker = widgets.DatePicker(description="Start date:", value=datetime.date.today(), style={'description_width':'initial'})
    days_slider = widgets.IntSlider(value=3, min=1, max=14, description="Days:", style={'description_width':'initial'})
    interests_sel = widgets.SelectMultiple(options=["culture","food","nature","shopping","landmark","relax"], description="Interests:", style={'description_width':'initial'})
    budget_dd = widgets.Dropdown(options=["low","medium","high"], value="medium", description="Budget:", style={'description_width':'initial'})
    activities_slider = widgets.IntSlider(value=3, min=1, max=5, description="Activities/day:", style={'description_width':'initial'})
    gen_btn = widgets.Button(description="Generate itinerary", button_style='success')
    save_btn = widgets.Button(description="Save as HTML", button_style='')
    output = widgets.Output(layout={'border':'1px solid #ddd', 'width':'900px', 'height':'520px', 'overflow':'auto'})

    def on_gen(b):
        with output:
            output.clear_output()
            city = city_dd.value
            start = start_picker.value or datetime.date.today()
            days = days_slider.value
            interests = list(interests_sel.value)
            budget = budget_dd.value
            per_day = activities_slider.value
            it = generate_itinerary(city, start, days, interests, budget, per_day)
            html = itinerary_to_html(city, start, days, it, interests, budget)
            display(HTML(html))
            # save HTML to object for save button
            output._last_html = html
            output._last_meta = (city,start,days)

    def on_save(b):
        with output:
            html = getattr(output, "_last_html", None)
            meta = getattr(output, "_last_meta", None)
            if not html:
                print("Generate an itinerary first.")
                return
            city,start,days = meta
            fname = f"itinerary_{city}_{start.isoformat()}.html".replace(" ", "_")
            with open(fname, "w", encoding="utf-8") as f:
                f.write(html)
            display(HTML(f"<div style='padding:8px;background:#e8f5e9;border-radius:6px;'>Saved: <b>{os.path.abspath(fname)}</b></div>"))

    gen_btn.on_click(on_gen)
    save_btn.on_click(on_save)

    controls = widgets.VBox([widgets.HBox([city_dd, start_picker, days_slider]), widgets.HBox([interests_sel, activities_slider, budget_dd]), widgets.HBox([gen_btn, save_btn])])
    display(widgets.HTML("<h2 style='font-family:Arial;color:#2c3e50;'>✨ AI Travel Planner (demo)</h2><div style='color:#555;'>Choose destination, dates and interests — click Generate to create a day-by-day plan.</div>"))
    display(controls, output)

def run_cli():
    print("Interactive CLI travel planner (simple).")
    city = input(f"Destination {list(ATTRACTIONS.keys())}: ").strip() or "Paris"
    start_str = input("Start date (YYYY-MM-DD) or leave blank for today: ").strip()
    start = datetime.date.fromisoformat(start_str) if start_str else datetime.date.today()
    days = int(input("Days (1-14): ") or "3")
    interests_input = input("Interests (comma-separated: culture,food,nature,shopping,landmark,relax) or leave blank for all: ").strip()
    interests = [s.strip() for s in interests_input.split(",")] if interests_input else []
    budget = input("Budget (low/medium/high) [medium]: ").strip() or "medium"
    per_day = int(input("Activities per day (1-5) [3]: ") or "3")
    it = generate_itinerary(city, start, days, interests, budget, per_day)
    html = itinerary_to_html(city, start, days, it, interests, budget)
    print("\nGenerated itinerary (HTML preview will not render in CLI). Save to file? (y/n)")
    if input().lower().startswith("y"):
        fname = f"itinerary_{city}_{start.isoformat()}.html".replace(" ", "_")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Saved: {os.path.abspath(fname)}")
    else:
        print("Done. You can open the HTML file to see formatted itinerary (or run the notebook UI).")

# Run appropriate interface
if HAS_WIDGETS:
    run_with_widgets()
else:
    run_cli()
