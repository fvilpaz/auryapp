<div align="right">
  <img src="https://img.shields.io/badge/EN-1a6fc4?style=flat-square" alt="English">
  &nbsp;<a href="MANUAL.es.md"><img src="https://img.shields.io/badge/ES-555555?style=flat-square" alt="Español"></a>
</div>

# User Manual — AuryApp

Complete guide for the daily use of the Beach Club management application.

---

## Access

Open your browser and go to the app's URL. Enter your username and password.

> If you enter the wrong password 5 times in a row, the account is automatically locked for 1 hour.

> The session closes automatically when you close the browser, and expires after 8 hours of inactivity regardless.

### Create a new account

If you don't have an account, click **Create new account** on the login screen. Fill in your first name, last name, username, email and password. Once registered, you are taken directly into the app.

> New accounts do not have administrator permissions. An administrator can grant them from the Admin panel.

The welcome greeting (Good morning / Good afternoon / Good evening) and the weather update automatically.

---

## Dashboard

The home screen shows a summary of the day:

- **Weather** — Temperature and weather conditions in Valencia (updated every 30 minutes)
- **Modules** — Quick access to all sections with the most important data from each
- **Points of sale** — Status of each area: who is working today and task progress
- **Upcoming events** — Table with events for the next few days
- **Notices** — Birthdays, approved holidays, single days off and contracts expiring soon

The dashboard modules display animations with relevant information (recent notes, today's staff, upcoming events...). They update automatically every 10 minutes.

---

## Visual themes

In the top-right corner, click your initials to open the user menu. From there you can change the app's theme:

| Theme | Style |
|-------|-------|
| Light | White and blue, default |
| Dark | Black background, blue icons |
| Mint | Mint green |
| Barbie | Pink |
| Dracula | Dark purple |
| Cyberpunk | Black and yellow |

Your choice is saved automatically for future visits.

---

## Agenda

Notes and reminders with priority. Access from the **Agenda** module on the dashboard.

### Add a note

1. Type the text in the text field
2. Select the priority:
   - **Urgent** — always appears at the top, red border
   - **Moderate** — yellow border
   - **Normal** — green border (default)
3. Click **Add note** or use `Ctrl + Enter`

### Dictate by voice

Click the microphone icon and speak. The text appears automatically in the field. Works in Chrome and Edge.

### Resolve a note

Click the ✓ icon on the note. It disappears from the main list and moves to the **Recently resolved** section at the bottom, with strikethrough text.

### Delete a note

Click the trash icon. The note is deleted without confirmation.

---

## Events

Management of celebrations: weddings, graduations, communions, galas, pre-weddings and others.

### View all events

Access from **Events** on the dashboard or in the menu.

### Create an event

1. Click **New event**
2. Fill in: client, type, concept, date, spaces, number of guests and notes
3. Save

### Event detail

From the event page you can:

- **Edit** the event data
- **Upload documents** (PDFs, images, quotes...)
- **Shifts and waitstaff** — add work groups (e.g. "Main hall") and assign waiters with their role
- **Floor plan** — visual editor to design the layout of the space

### Floor plan (visual editor)

The editor lets you design the table and space layout for each event.

#### Add elements

Click a toolbar button to enter placement mode — the cursor changes to a **crosshair**. Then click anywhere on the canvas to place the element at that exact position. Press `Escape` to cancel without placing.

| Element | Description |
|---------|-------------|
| Round table | Circular table with label |
| Rectangular table | Rectangular table with label |
| Cocktail | Tall cocktail table |
| Stage | Stage area (unique) |
| Bar | Venue bar (unique) |
| DJ | DJ booth (unique) |
| TV | Television (unique) |
| Speaker | Ambient speaker |
| Zone | Named resizable area (coloured box with label) |
| Column | Structural column |
| Plant | Decorative plant element |
| Guest entrance | Guest access point (unique) |
| Guest exit | Guest exit point (unique) |
| Staff entrance | Service staff access (unique) |
| Staff exit | Service staff exit (unique) |
| Text | Free editable text |

#### Add in batch

Click **Add batch** to place multiple tables at once. Choose the type, quantity and arrangement:
- **Horizontal** — row from left to right
- **Vertical** — column from top to bottom
- **Circle** — arranged in a circle around the point where you click

#### Table information

Click on a table to select it. The **Info panel** opens on the right with fields for:
name, range, number of guests, meat, fish, vegetarian, children, coeliacs, allergies and notes.

The number of guests is also shown as a badge directly below the table on the canvas, updated in real time.

Changes are saved instantly when you click outside the field or close the panel.

#### Edit all tables

Click **Edit tables** (from the event detail page) to see all the floor plan's tables in a single table view. Each row has the same fields as the Info panel. Changes save automatically row by row (no save button needed).

#### Multi-selection

Hold `Shift` and click multiple elements, or drag a selection rectangle to select several at once. With multiple elements selected:
- **Delete** (`Del` key or trash button) removes all of them at once
- **Colour swatch** applies the new colour to all selected elements at once

#### Entrance and exit labels

The labels for guest and staff entrances/exits are always displayed horizontally below the element, regardless of how the element is rotated.

#### Other actions

- **Move elements** — drag with your finger (mobile/tablet) or with the mouse
- **Resize** — drag the corners of the selected object
- **Change colour** — select the object and use the colour picker in the toolbar
- **Rename** — double-click any element to rename it
- **Delete** — select and press `Del` or the trash button
- **Undo / Redo** — ↩ ↪ buttons in the toolbar
- **Lock** — activate lock mode to prevent elements from being moved accidentally while scrolling
- **Zoom** — pinch with two fingers on mobile/tablet or use the mouse wheel
- **Save** — saves automatically whenever an element is modified
- **Export** — download the floor plan as a PNG image or PDF (labels and pax badges included)

---

## Shift schedule

Weekly view of all employees and their shifts.

### Navigate between weeks

Use the **←** **→** arrows to move week by week.

### Assign a shift

Click on an employee's day and select the shift type.

### Shift colours

Each shift type has a distinct colour in the schedule:

| State | Colour |
|-------|--------|
| Work | Employee's colour (green by default) |
| Day off | Purple |
| Immovable | Orange |
| Holidays | Yellow |
| Day off + holidays | Light orange |
| Long weekend | Lilac |
| Sick leave | Red |

### Assign a space to an employee

From the space page or from the schedule, drag the employee to the corresponding space.

---

## Staff

Management of the club's workforce.

### Employee profile

Each employee has: first name, last name, role, phone, email, date of birth, contract type and expiry date (if applicable).

Additional fields relevant to the schedule:

- **Colour** — the colour that represents the employee in the schedule when working (green by default)
- **Weekly hours** — contract hours (40 or 30); used to calculate availability

### Expiry alerts

On the dashboard (section **Expiries**) the contracts expiring in the coming days are shown. Expired ones appear in red.

---

## Holidays and single days off

### Request time off (as an employee)

1. Go to the employee's profile
2. Click **New request**
3. Select type (holidays / day off / free day...), dates and optional notes
4. The request is saved in **Pending** status

### Approve or reject (as admin)

From **Holidays** or **Days off** in the menu, you will see all pending requests with buttons to approve or reject them.

Approved requests appear on the dashboard under **Notices**.

---

## Tasks

Opening and closing checklists per space. Generated automatically every day.

### Mark a task as completed

Click on the task. It is marked instantly (without reloading the page). The progress bar for the space updates on the dashboard.

### View tasks for a space

Access from **Points of sale** on the dashboard or from **Spaces** in the menu.

---

## Orders

Record of items needed per point of sale.

### Add an item

1. Enter the space from **Orders**
2. Click **New item**
3. Enter name and quantity

### Update quantity

Use the **+** and **−** buttons directly in the list. It saves instantly.

---

## Calendar

Monthly view of all events. Navigate with the month arrows. Click on an event to see its detail.

---

## Administration panel

If your account has staff permissions, the **Admin** button (with a shield icon) appears in the top bar. From there you can manage users, groups and all the app's models directly.

---

## Log out

Click your initials (top-right corner) and click **Log out**.

---

## Support

Developed by **Fernando Vilas Paz**  
[GitHub](https://github.com/fvilpaz) · [LinkedIn](https://www.linkedin.com/in/fernando-vilas-paz-1626901a9)
