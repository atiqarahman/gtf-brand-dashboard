# GTF Brand Dashboard — Complete Vibe Coding Prompt

Build a complete Brand Dashboard for Get The Fit (GTF), a fashion marketplace. This is what brand partners see when they log in to manage their products, orders, and payouts. Use Next.js + Tailwind CSS + shadcn/ui components. Dark sidebar, light main content, clean and professional.

## Design Language
- Sidebar: dark (#1a1a1a) with white text
- Main content: white/light grey background (#f5f5f5)
- Accent color: GTF purple (#7C3AED) for buttons, badges, active states
- Warm olive for primary CTAs (#3B4021 background, #FCFBF0 text)
- Font: Inter or system font stack
- Border radius: 8px for cards, 4px for inputs
- Shadows: subtle, 0 1px 3px rgba(0,0,0,0.1)

## Layout Structure

### Sidebar (fixed, 240px wide)
- Top: "GTF BRAND PORTAL" text + brand name below (e.g., "ITRH")
- Navigation items with icons:
  - 📦 Orders (with red badge for new order count)
  - 📝 Custom Requests (with badge for pending count)
  - 📊 Products
  - 💰 Payouts
  - 📄 Invoices
  - ⚙️ Settings
- Bottom: "Need Help? Contact GTF" link

### Header (top bar)
- Left: Current page title (e.g., "Orders")
- Right: Bell icon with red notification badge (unread count), brand avatar/initials, "Log Out" button
- Notification dropdown on bell click: list of recent notifications, each clickable → navigates to relevant page, "Mark all as read" at top

---

## Tab 1: Orders

### Orders List View
- Yellow banner at top: "⚠️ Ship orders within 48 hours of receiving them"
- Filter dropdown: All | New | Shipped | Delivered | Cancelled
- Search bar: search by order number or customer name

**Table columns:**
| Order | Customer | Destination | Items | Your Payout | Status | Actions |

- Order: #BO-ITRH-2026-XXXX format, with date below
- Customer: name
- Destination: country flag emoji + city/country
- Items: "2 items" count
- Your Payout: "AED 2,010" with small text "(after X% commission)" below — commission rate is variable per brand
- Status: colored badge — NEW (red), CONFIRMED (blue), SHIPPED (amber), IN TRANSIT (purple), DELIVERED (green), CANCELLED (grey)
- Actions: "View & Ship" button for new orders, "Track" for shipped, "Details" for delivered

### Order Detail View
- Back button: "← Back to Orders"
- Header: Order number + status badge
- Two columns:

**Left column:**
- ITEMS TO SHIP section: product image thumbnail (60px), product name, SKU, size, color, quantity, price per item
- SHIP TO section: customer full name, address line 1, line 2, city, country, postal code, phone number

**Right column:**
- YOUR PAYOUT section:
  - Order Total: AED X,XXX
  - GTF Commission (X%): -AED XXX (percentage varies per brand)
  - **Your Payout: AED X,XXX** (bold, large)
  - Note: "Payout available after delivery + 14-day return window"

**Action buttons at bottom:**
- "Cancel" (secondary, grey) — opens confirmation modal: "Cancel this order? Customer will receive store credit."
- "Print Packing Slip" (secondary, outlined) — generates packing slip PDF that goes INSIDE the package
- "Download Proforma Invoice" (text link) — downloads proforma PDF
- "Download Shipping Documents" (text link) — all customs/shipping docs per Indian logistics guide
- **"Print DHL Label & Mark Shipped"** (primary, large, olive green #3B4021) — generates DHL label, marks order as shipped, auto-generates final invoice, sends customer notification

---

## Tab 2: Custom Requests

### Custom Requests List
- Table: Request ID, Customer, Product, Status, Date, Actions
- Status badges: PENDING (amber), IN CONVERSATION (blue), APPROVED (green), EXPIRED (grey), PAYMENT SENT (purple)
- Action: "Open Chat" button

### Custom Request Detail — Chat View
- Split layout:
  - **Left (40%):** Product card showing image, name, SKU, original price, customer's measurement notes, custom request description
  - **Right (60%):** Chat interface between brand and customer

**Chat interface:**
- Message bubbles: Brand messages right-aligned (purple bg), Customer messages left-aligned (grey bg)
- Each message shows sender name + timestamp
- Text input at bottom with "Send" button
- Auto-expire notice: "This request expires in X days" (countdown from 5 days)
- If expired: "This request has expired" banner, chat becomes read-only

**Brand action buttons (above chat input):**
- "Add Customisation Cost" — opens modal: input field for additional amount (AED), notes field, "Confirm" button
- "Send Payment Link" — disabled until price confirmed. Sends customer: product price + custom amount. Generates proforma invoice.
- "Decline Request" — opens modal with optional reason text

**After customer pays:**
- Status changes to "PAID — Awaiting Production"
- Order appears in Orders tab as a new order with "CUSTOM" badge
- Normal order flow from there (ship, track, deliver)

---

## Tab 3: Products

### Product List View
- "Import CSV" button (top right, primary) — opens upload modal
- "Add Product" button (secondary) — disabled after 5 manually added products, tooltip: "Maximum 5 manual additions. Use CSV import for bulk."
- Search bar: search by product name or SKU
- Filter: All | Live | Draft | Pending Review | Archived

**Product table:**
| Image | Product Name | SKU | Price | Sizes | Stock | Vibes | Status | Actions |

- Image: 50px thumbnail
- Product Name: clickable, truncated with tooltip
- SKU: GTF-BRAND-XXX
- Price: editable inline — clicking opens small input, saves on blur, notifies GTF admin
- Sizes: pills showing available sizes (XS, S, M, L, XL)
- Stock: number, turns red if <5
- Vibes: small colored pills (Old Money, Glam, etc.) — visible but NOT editable by brand
- Status: dropdown — Live | Archived (changing to Archived notifies GTF admin)
- Actions: "View Details" link

**Status indicator colors:**
- Draft: grey
- Pending Review: amber with "Some attributes need GTF review" tooltip
- Live: green
- Archived: dark grey, strikethrough on product name

### CSV Import Flow
1. Brand clicks "Import CSV"
2. Modal opens: drag-and-drop zone + "Browse Files" button + "Download Template" link
3. Brand uploads CSV/XLSX
4. **Processing screen:** Progress bar "Processing 23/50 products..." with product name scrolling below
5. **If errors:** Error report table showing:
   - Row number
   - Field with error
   - Error description (e.g., "Missing price", "Invalid image link", "Weight required")
   - "Download Error Report" button
   - "Re-upload Corrected File" button
6. **If success:** "✅ 50 products imported successfully! They are now in Draft status and will be reviewed by GTF."

### Product Detail View
- Back button
- Large product images (carousel)
- All v4 attributes displayed in organized sections:
  - **Hard Attributes:** Category, Colors, Material, Details, Silhouette, Length, Neckline, Sleeve, Pattern, Price Tier
  - **Soft Attributes:** Vibes, Keywords, Occasions, Style References, Destinations, Modesty Level
- Each attribute has a small "Flag for Review" icon — brand can click to flag a disagreement with AI extraction
- Flagged attributes show amber highlight with brand's note

---

## Tab 4: Payouts

### Payout Summary (3 cards at top)
| PENDING | AVAILABLE | PAID (This Month) |
| AED X,XXX | AED X,XXX | AED XX,XXX |
| X orders | Ready to pay | This month |

- Info banner: "ℹ️ Payouts processed every Monday. Orders become available 14 days after delivery (return window)."

### Pending Orders Table
| Order | Your Payout | Delivered | Available Date |
- Shows countdown to when each order's payout becomes available

### Payout History Table
| Date | Amount | Orders | Status | Receipt |
- Status: ✅ Paid (green), ⏳ Scheduled (amber)
- Receipt: "Download" link for each payout

---

## Tab 5: Invoices

### Invoice Download Center
- Search: by order number, customer name, or date range
- Filter: Proforma | Final | All
- Date range picker

**Invoice table:**
| Order | Customer | Type | Amount | Date | Download |
- Type: "Proforma" (blue badge) or "Final" (green badge)
- Download: PDF download button

- Proforma invoices generated at every customer payment
- Final invoices generated when brand marks order as shipped
- Both available for download immediately

---

## Tab 6: Settings

### Brand Information
- Brand Name (read-only)
- Contact Email (editable)
- Contact Phone (editable)
- Shipping Origin: city, country (editable)
- Commission Rate (read-only, shown for transparency)

### Payout Details
- Bank Name
- Account Number (masked: ****4567)
- Routing/IFSC Code
- "Edit Bank Details" button — opens form with verification

### Notification Preferences
Toggle switches:
- ☑️ Email for new orders (default ON)
- ☑️ Email for custom requests (default ON)
- ☑️ Email for returns (default ON)
- ☑️ Email for low stock alerts (default ON)
- ☐ Daily order summary email
- ☐ Weekly review digest email

### Security
- Change Password button
- Active sessions list

---

## Notification System

### Bell Icon (header, always visible)
- Red badge with unread count
- Click: dropdown panel slides down, max 10 recent notifications
- Each notification: icon + title + time ago + clickable → navigates to relevant page
- "Mark all as read" button at top
- "View all" link at bottom → opens full notification page

### Notification Types:
- 🔔 New Order: "New order #BO-XXXX from [Customer] — AED X,XXX"
- 💬 Custom Request: "New customisation request for [Product]"
- 💬 Custom Reply: "[Customer] replied to your custom request"
- ⏰ Custom Expiring: "Custom request for [Product] expires tomorrow"
- 📦 Return Initiated: "[Customer] initiated a return for [Product]"
- 💰 Payout Processed: "AED X,XXX has been transferred to your bank"
- ⚠️ Low Stock: "[Product] — only X units left in [Size]"
- ❌ Out of Stock: "[Product] [Size] is now out of stock"
- ✅ CSV Import: "50 products imported successfully"
- ❌ CSV Errors: "CSV import found 3 errors — review required"

---

## Data/Mock Data

Use this sample data for the demo:

**Brand:** ITRH (In The Raw House), ships from New Delhi, India
**Commission rate:** 25%

**Sample products:**
- Silk Midi Dress, SKU: GTF-ITRH-001, AED 1,050, Vibes: [Old Money, Wedding Guest]
- Embroidered Anarkali Set, SKU: GTF-ITRH-002, AED 1,983, Vibes: [Dubai Glam, Wedding Guest]
- Cotton Kurta Set, SKU: GTF-ITRH-003, AED 529, Vibes: [Elevated Basics]
- Linen Blouse, SKU: GTF-ITRH-004, AED 385, Vibes: [Cool Girl]

**Sample orders:**
- #BO-ITRH-2026-0087, Sarah Johnson, Dubai UAE, 2 items, AED 2,512, Status: NEW
- #BO-ITRH-2026-0085, Aisha Khan, Abu Dhabi UAE, 1 item, AED 1,050, Status: SHIPPED
- #BO-ITRH-2026-0082, Emma Williams, London UK, 3 items, AED 3,400, Status: DELIVERED

**Sample custom request:**
- Customer: Priya Sharma, Product: Silk Midi Dress, Request: "Can you make this in a longer maxi length? My measurements: Height 5'7, Bust 36, Waist 28"
