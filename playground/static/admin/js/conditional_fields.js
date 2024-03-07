(function($) {
    $(document).ready(function() {
        var amcExistField = $('#id_AMC_exist');
        var amcTypeField = $('#id_AMC_type');
        var warrantyExistField = $('#id_Warranty_exist');
        var warrantyTypeField = $('#id_Warranty_type');
        var warrantyProviderField = $('#id_warranty_provider');

        function toggleAMCFields() {
            if (amcExistField.val() === 'Y') {
                amcTypeField.closest('.form-row').show();
                warrantyProviderField.closest('.form-row').show();
            } else {
                amcTypeField.closest('.form-row').hide();
                warrantyProviderField.closest('.form-row').hide();
            }
        }

        function toggleWarrantyFields() {
            if (warrantyExistField.val() === 'Y') {
                warrantyTypeField.closest('.form-row').show();
                warrantyProviderField.closest('.form-row').show();
            } else {
                warrantyTypeField.closest('.form-row').hide();
                warrantyProviderField.closest('.form-row').hide();
            }
        }

        // Initial toggling
        toggleAMCFields();
        toggleWarrantyFields();

        // Event listeners for changes in dropdowns
        amcExistField.on('change', toggleAMCFields);
        warrantyExistField.on('change', toggleWarrantyFields);
    });
})(django.jQuery);
