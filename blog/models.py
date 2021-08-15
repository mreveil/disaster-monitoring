from django.db import models

# Create your models here.

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class BlogIndex(Page):
    subpage_types = ["blog.BlogPage"]  # , "blog.BlogArchivePage"]
    template = "blog_index.html"


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
    ]

    template = "blog_page.html"


class BlogPage(Page):

    # Database fields

    body = RichTextField()
    intro = models.CharField(max_length=250)
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField("body"),
        index.FilterField("date"),
    ]

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body", classname="full"),
        InlinePanel("related_links", label="Related links"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel("feed_image"),
    ]

    # HTML template
    template = "blog_page.html"

    # Parent page / subpage type rules

    parent_page_types = ["blog.BlogIndex"]
    subpage_types = []


class BlogPageRelatedLink(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name="related_links")
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel("name"),
        FieldPanel("url"),
    ]
