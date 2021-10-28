"""
Configuration file to scrape news website data using span tag class attributes
"""

NEWS_ARCHIVE_ATTRS = {
    "International" : {
        "title_span_class_attrs" : "block text-primary-base dark:text-dm-primary-base hover:text-primary-dark focus:text-primary-darker font-brandUI font-extrabold lg:text-xl md:text-xl sm:text-l leading-tight mb-8",
        "sub_title_span_class_attrs" : "align-middle hover:opacity-moderate focus:opacity-moderate",
        "abstract_span_class_attrs" : "font-serifUI font-normal lg:text-l md:text-base sm:text-base leading-loose mr-6"
    },
    "Others" : {
        "title_span_class_attrs" : "block text-primary-base dark:text-dm-primary-base focus:text-primary-darker hover:text-primary-dark font-sansUI font-bold text-base",
        "sub_title_span_class_attrs" : "align-middle",
        "abstract_span_class_attrs" : "font-serifUI font-normal text-base leading-loose mr-6"
    }
}