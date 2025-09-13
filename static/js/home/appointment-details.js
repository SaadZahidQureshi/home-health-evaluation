 let successModal;
        let nextActionsModal;

        // Initialize modals when DOM is ready
        document.addEventListener('DOMContentLoaded', function() {
            successModal = new bootstrap.Modal(document.getElementById('successModal'));
            nextActionsModal = new bootstrap.Modal(document.getElementById('nextActionsModal'));
        });

        // Open success modal
        function openSuccessModal() {
            successModal.show();
        }

        // Continue to next button action
        function continueToNext() {
            console.log('Continue to next clicked');
            successModal.hide();
            // Add your custom logic here
        }

        // Save to calendar button action
        function saveToCalendar() {
            console.log('Save to calendar clicked');
            successModal.hide();
            setTimeout(() => {
                nextActionsModal.show();
            }, 300);
        }

        // Go back from second modal
        function goBack() {
            nextActionsModal.hide();
            setTimeout(() => {
                successModal.show();
            }, 300);
        }

        // Action handlers for second modal
        function editInformation() {
            console.log('Edit Information clicked');
            nextActionsModal.hide();
            // Add your custom logic here
        }

        function reschedule() {
            console.log('Reschedule clicked');
            nextActionsModal.hide();
            // Add your custom logic here
        }

        function cancelAppointment() {
            console.log('Cancel Appointment clicked');
            nextActionsModal.hide();
            // Add your custom logic here
        }

        function scheduleNew() {
            console.log('Schedule New Appointment clicked');
            nextActionsModal.hide();
            // Add your custom logic here
        }