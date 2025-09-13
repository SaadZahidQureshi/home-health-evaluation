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
        
        this.init();
        this.setupEventListeners();
        this.handleResize();
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
        
        // Generate 60 days from today
        for (let i = 0; i < 60; i++) {
            const date = new Date(today);
            date.setDate(today.getDate() + i);
            this.dates.push(date);
        }
    }
    
    renderDates() {
        this.datesContainer.innerHTML = '';
        
        const visibleDates = this.dates.slice(
            this.currentStartIndex, 
            this.currentStartIndex + this.maxVisibleDates
        );
        
        visibleDates.forEach((date, index) => {
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
        
        // Format the date display
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
                this.selectedDate = new Date(this.dates[currentSelectedIndex - 1]);
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
                this.selectedDate = new Date(this.dates[currentSelectedIndex + 1]);
                this.updateMonthTitle();
            }
            
            this.renderDates();
            this.updateArrowStates();
        }
    }
    
    updateArrowStates() {
        // Left arrow disabled if at the beginning (current date)
        if (this.currentStartIndex === 0) {
            this.leftArrow.classList.add('disabled');
            this.leftArrow.disabled = true;
        } else {
            this.leftArrow.classList.remove('disabled');
            this.leftArrow.disabled = false;
        }
        
        // Right arrow enabled as long as there are more dates
        if (this.currentStartIndex + this.maxVisibleDates >= this.dates.length) {
            // Generate more dates if needed
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


document.addEventListener('DOMContentLoaded', () => new ResponsiveCalendar());