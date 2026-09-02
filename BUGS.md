# Bugs found

Add one section per issue. Bug 1 is filled in to show the format — fix it, then write what you changed. Copy the blank template for the rest.

Keep this file in the repo and **commit it** with your fixes.

---

## Bug 1

**How to reproduce:** Open the app. The expense list says “Newest first”. The first row is Wine (7 Mar). Board game (15 Mar) is further down.

**What is wrong:** The list is showing oldest expenses first. Newest should be at the top.

**What I changed:** Our dateValue(date) function was not parsing the value of the date in the Date format, which i changed and get the desired list order.

## Bug 2

**How to reproduce:** Open the app. In the Balance sheet whenever we were sharing the expenses on Split equally the list is updating wrong,  

**What is wrong:** The logic to split the expenses was working fine for the remaining selected people except the person who has been selected as the Paid by, his balance was increasing/decreasing with respect to the expense amount that has been typed in the amount box. 

**What I changed:** The person who was selected was getting added explicitly, the amount that was getting splited between the selected people. I have removed that part and added in the for loop to be managed inside the loop.

---
