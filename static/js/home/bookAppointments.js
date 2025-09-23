class ResponsiveCalendar {
    constructor() {
        this.currentDate = new Date();
        this.selectedDate = new Date();
        this.currentStartIndex = 0;
        this.dates = [];
        this.maxVisibleDates = this.getMaxVisibleDates();
        
        this.monthTitle = document.getElementById('monthTitle');
        this.datesContainer = document.getElementById('datesContainer');
        this.leftArrow = document.getElementById('leftArrow');
        this.rightArrow = document.getElementById('rightArrow');
        this.slotsContainer = document.querySelector('.slots'); // ✅ slots area

        this.init();
        this.setupEventListeners();
        this.handleResize();

        // Load slots for today's date on page load
        this.fetchSlots(this.selectedDate);
    }

    init() {
        this.generateDates();
        this.renderDates();
        this.updateMonthTitle();
        this.updateArrowStates();
    }

    getMaxVisibleDates() {
        const width = window.innerWidth;
        if (width >= 1024) return 7;
        if (width >= 641) return 5;
        if (width >= 481) return 3;
        return 1;
    }

    generateDates() {
        this.dates = [];
        const today = new Date();
        let count = 0;

        // Jab tak 60 weekdays generate na ho jayein
        while (this.dates.length < 60) {
            const date = new Date(today);
            date.setDate(today.getDate() + count);

            const dayOfWeek = date.getDay(); 
            // Sunday = 0, Monday = 1, ..., Saturday = 6
            if (dayOfWeek !== 0 && dayOfWeek !== 6) {
                this.dates.push(date);
            }

            count++;
        }
    }


    renderDates() {
        this.datesContainer.innerHTML = '';
        const visibleDates = this.dates.slice(
            this.currentStartIndex, 
            this.currentStartIndex + this.maxVisibleDates
        );

        visibleDates.forEach((date) => {
            const dateElement = this.createDateElement(date);
            this.datesContainer.appendChild(dateElement);
        });
    }

    createDateElement(date) {
        const dateDiv = document.createElement('div');
        dateDiv.className = 'date';

        if (this.isSameDay(date, this.selectedDate)) {
            dateDiv.classList.add('selected');
        }

        const weekday = date.toLocaleDateString('en-US', { weekday: 'short' });
        const day = date.getDate();
        const month = date.toLocaleDateString('en-US', { month: 'short' });

        dateDiv.textContent = `${weekday} ${day} ${month}`;
        dateDiv.dataset.value = date.toISOString();

        dateDiv.addEventListener('click', () => this.selectDate(date));

        return dateDiv;
    }

    selectDate(date) {
        this.selectedDate = new Date(date);
        this.updateMonthTitle();
        this.renderDates();
        this.ensureSelectedDateVisible();

        // ✅ fetch slots for selected date
        this.fetchSlots(this.selectedDate);
    }

    async fetchSlots(date) {
        const formattedDate = date.toISOString().split('T')[0];
        const url = `/api/availability/check-date?date=${formattedDate}`;

        try {
            const response = await fetch(url);
            const data = await response.json();
            this.renderSlots(data.slots);
        } catch (error) {
            console.error("Error fetching slots:", error);
        }
    }

    renderSlots(slots) {
        this.slotsContainer.innerHTML = ""; // clear old slots
        console.log("Fetched slots:", slots);

        slots.forEach((slot, index) => {
            // create input + label
            const input = document.createElement("input");
            input.type = "radio";
            input.value = slot.slot_type;
            input.name = "available_slot";
            input.className = "slot-input";
            input.id = `slot_${index}`;
            input.disabled = slot.is_booked; // disable if booked

            const label = document.createElement("label");
            label.className = "slot";
            label.htmlFor = input.id;
            // label.dataset.slotId = slot.id;
            label.textContent = slot.slot_display;

            if (slot.is_booked) {
                label.classList.add("faded"); // make faded
            }

            this.slotsContainer.appendChild(input);
            this.slotsContainer.appendChild(label);
        });
    }

    ensureSelectedDateVisible() {
        const selectedIndex = this.dates.findIndex(date => 
            this.isSameDay(date, this.selectedDate)
        );
        if (selectedIndex === -1) return;

        const endIndex = this.currentStartIndex + this.maxVisibleDates - 1;

        if (selectedIndex < this.currentStartIndex) {
            this.currentStartIndex = selectedIndex;
            this.renderDates();
            this.updateArrowStates();
        } else if (selectedIndex > endIndex) {
            this.currentStartIndex = selectedIndex - this.maxVisibleDates + 1;
            this.renderDates();
            this.updateArrowStates();
        }
    }

    navigateLeft() {
        if (this.currentStartIndex > 0) {
            this.currentStartIndex--;

            const currentSelectedIndex = this.dates.findIndex(date => this.isSameDay(date, this.selectedDate));
            if (currentSelectedIndex > 0) {
                this.selectDate(new Date(this.dates[currentSelectedIndex - 1]));
                this.updateMonthTitle();
            }

            this.renderDates();
            this.updateArrowStates();
        }
    }

    navigateRight() {
        if (this.currentStartIndex + this.maxVisibleDates < this.dates.length) {
            this.currentStartIndex++;

            const currentSelectedIndex = this.dates.findIndex(date => this.isSameDay(date, this.selectedDate));
            if (currentSelectedIndex < this.dates.length - 1) {
                this.selectDate(new Date(this.dates[currentSelectedIndex + 1]));
                this.updateMonthTitle();
            }

            this.renderDates();
            this.updateArrowStates();
        }
    }

    updateArrowStates() {
        if (this.currentStartIndex === 0) {
            this.leftArrow.classList.add('disabled');
            this.leftArrow.disabled = true;
        } else {
            this.leftArrow.classList.remove('disabled');
            this.leftArrow.disabled = false;
        }

        if (this.currentStartIndex + this.maxVisibleDates >= this.dates.length) {
            const lastDate = this.dates[this.dates.length - 1];
            for (let i = 1; i <= 30; i++) {
                const newDate = new Date(lastDate);
                newDate.setDate(lastDate.getDate() + i);
                this.dates.push(newDate);
            }
        }
    }

    updateMonthTitle() {
        const options = { month: 'long', year: 'numeric' };
        this.monthTitle.textContent = this.selectedDate.toLocaleDateString('en-US', options);
    }

    isSameDay(date1, date2) {
        return date1.toDateString() === date2.toDateString();
    }

    setupEventListeners() {
        this.leftArrow.addEventListener('click', () => {
            if (!this.leftArrow.disabled) {
                this.navigateLeft();
            }
        });

        this.rightArrow.addEventListener('click', () => {
            this.navigateRight();
        });

        window.addEventListener('resize', () => {
            this.handleResize();
        });
    }

    handleResize() {
        const newMaxVisible = this.getMaxVisibleDates();
        if (newMaxVisible !== this.maxVisibleDates) {
            this.maxVisibleDates = newMaxVisible;
            this.ensureSelectedDateVisible();
            this.renderDates();
            this.updateArrowStates();
        }
    }
}

let calendarObj = new ResponsiveCalendar();

// document.addEventListener('DOMContentLoaded', () => new ResponsiveCalendar());


function selectSlot() {
    const selectedSlot = document.querySelector('input[name="available_slot"]:checked');
    if (selectedSlot) {
        const slotValue = selectedSlot.value;
        sessionStorage.setItem("selected_slot", slotValue);
        sessionStorage.setItem("selected_date", calendarObj.selectedDate.toISOString().split('T')[0]);
        // Do something with the selected slot value
        console.log("Selected slot:", slotValue);
        location.pathname = '/appointment-details/';
    } else {
        console.log("No slot selected");
    }
}