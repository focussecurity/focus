from django import template
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from app.hourregistrations.helpers import get_month_by_number

register = template.Library()


@register.tag
def require_valid_date_for_edit(parser, token):
    try:
        tag_name, object = token.split_contents()

    # Raise an error if we don't have the correct params
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument (object)" % token.contents.split()[0]

    # Fetch everything from this tag to end_require
    nodelist = parser.parse(('end_require',))
    parser.delete_first_token()

    return DateValidForEdtNode(nodelist, object)


class DateValidForEdtNode(template.Node):
    """
    Node for require_permission tag
    """

    def __init__(self, nodelist, object):
        self.nodelist = nodelist
        self.object = template.Variable(object)

    def render(self, context):
        # If the object param resolves into an actual object, use that to check
        # if the user has permission

        try:
            object = self.object.resolve(context)

            if context['user'].has_permission_to("EDIT", object) and context['user'].canEditHourRegistration(object):
                return self.nodelist.render(context)
            else:
                return ''

        except template.VariableDoesNotExist:
            return ''


@register.tag
def month_title_with_arrows(parser, token):
    """

    Usage:
        {% month_title_with_arrows year month %}

    """

    # Extract the params
    try:
        tag_name, year, month, week, day = token.split_contents()

    # Raise an error if we don't have the correct params
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly two argument (object)" % token.contents.split()[0]

    return month_title_with_arrows_node(year, month, week, day)


class month_title_with_arrows_node(template.Node):
    """
    Node for require_permission tag
    """

    def __init__(self, year, month, week, day):
        self.year = template.Variable(year)
        self.month = template.Variable(month)
        self.week = template.Variable(week)
        self.day = template.Variable(day)

    def render(self, context):
        month = int(self.month.resolve(context))
        year = int(self.year.resolve(context))
        week = int(self.month.resolve(context))
        day = int(self.day.resolve(context))

        try:
            string = ""

            previousMonth = month - 1
            previousYear = year
            if(month == 1):
                previousMonth = 12
                previousYear = year - 1

            string += "<a href='%s'> < </a>" % (
            urlresolvers.reverse('app.hourregistrations.views.calendar',
                                 args=("%s" % previousYear, "%s" % previousMonth, week, day)))

            string += "%s %s" % (get_month_by_number(month), year)

            nextMonth = month + 1
            nextYear = year
            if(month == 12):
                nextMonth = 1
                nextYear = year + 1

            string += "<a href='%s'> > </a>" % (
            urlresolvers.reverse('app.hourregistrations.views.calendar',
                                 args=("%s" % nextYear, "%s" % nextMonth, week, day)))

            return string

        except template.VariableDoesNotExist:
            return ''


@register.tag
def links_for_archived_month(parser, token):
    """

    Usage:
        {% link_for_archived_month year month %}

    """

    # Extract the params
    try:
        tag_name, year, month = token.split_contents()

    # Raise an error if we don't have the correct params
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly two argument (object)" % token.contents.split()[0]

    return linksForArchivedMonth(year, month)


class linksForArchivedMonth(template.Node):
    """
    Node for require_permission tag
    """

    def __init__(self, year, month):
        self.year = template.Variable(year)
        self.month = template.Variable(month)

    def render(self, context):
        months = (self.month.resolve(context))
        year = int(self.year.resolve(context))

        try:
            string = ""
            for month in sorted(months):
                string += " <a href='%s'>%s</a>" % (
                urlresolvers.reverse('app.hourregistrations.views.viewArchivedMonth', args=("%s" % year, "%s" % month)),
                get_month_by_number(month))

            return string

        except template.VariableDoesNotExist:
            return ''