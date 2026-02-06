# Tahwill Clothing & Sportswear

Welcome to the **Tahwill Clothing** project.

## 🌐 Live Website

You can view the live website here:  
👉 **[https://tahwillclothing-oss.github.io/](https://tahwillclothing-oss.github.io/)**

This is where your customers will see the products.

## 📂 GitHub Repository (Control Panel)

To change products or edit files, go here:  
👉 **[https://github.com/tahwillclothing-oss/tahwillclothing-oss.github.io](https://github.com/tahwillclothing-oss/tahwillclothing-oss.github.io)**

---

## 🛠 How to Add or Change Products

You do not need to install anything. You can manage your inventory directly on **GitHub** (the link above).

### Step 1: Go to the Data File
1. Click on the **`data`** folder in the list of files above.
2. Click on **`inventory.json`**.

### Step 2: Edit the File
1. Click the **Pencil Icon (🖊️)** on the top right of the file view to start editing.
2. You will see a list of products code.

### Step 3: Add a New Product
To add a new item, copy the code block below and paste it into the list (make sure to paste it inside the main square brackets `[ ... ]`, after a comma `,`).

**Template to Copy:**
```json
{
    "id": 99,
    "title": "New Item Name",
    "price": 500,
    "originalPrice": 700,
    "cat": "t-shirt",
    "description": "Short description here.",
    "images": [
        "img_items/YourImage.jpg"
    ],
    "colors": [
        { "name": "Black", "hex": "#000000" }
    ],
    "sizes": ["S", "M", "L", "XL"],
    "launchDate": "2024-03-01",
    "outOfStock": false
}
```

### Step 4: Save Changes
1. Scroll to the bottom of the page.
2. Click the green button **"Commit changes..."**.
3. Your changes will be saved and the website will update shortly!

> [!IMPORTANT]
> **Check for Errors!** 
> If you miss a comma `,` or a quote `"`, the site will stop working.
> Before saving, copy all your code and paste it into **[JSON Grid](https://jsongrid.com/json-grid)**. It will tell you if the code is correct.
