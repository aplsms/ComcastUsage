command: """
    ComCap.widget/lib/comcap.py
"""

refreshFrequency: 30*60*1000

style: """
    // Change bar height
    bar-height = 8px

    // Align contents left or right
    widget-align = right

    // Position this where you want
    bottom  50px
    right   300px

    // Statistics text settings
    color #fff
    font-family Helvetica Neue
    background rgba(#000, .5)
    padding 10px 10px 15px
    border-radius 5px

    .container
        width: 300px
        text-align: widget-align
        position: relative
        clear: both

    .widget-title
        text-align: center

    .stats-container
        width: 100%
        margin-bottom 5px
        border-collapse collapse

    td
        font-size: 14px
        font-weight: 300
        color: rgba(#fff, .9)
        text-shadow: 0 1px 0px rgba(#000, .7)
        text-align: widget-align

    .widget-title
        font-size 10px
        text-transform uppercase
        font-weight bold
        color: #fff

    .stat
        width: 50%
        .down
            float: left
            text-align left
        .up
            float: right
            text-align right

    .label-cup
        font-size 12px
        // text-transform uppercase
        font-weight bold
        float: left
        align: left

    .label-limit
        font-size 12px
        //text-transform uppercase
        font-weight bold
        float: right
        align: right

    .bar-container
        width: 100%
        height: bar-height
        border-radius: bar-height
        clear: both
        background: rgba(#fff, .5)
        position: absolute
        margin-bottom: 5px

    .bar-container-2
        width: 100%
        height: 1px
        border-radius: bar-height
        clear: both
        background: rgba(#fff, .5)
        position: absolute
        margin-bottom: 3px

    .bar
        height: bar-height
        transition: width .2s ease-in-out
        border-radius: bar-height 0 0 bar-height
        float: left

    .bar:last-child
        border-radius: 0 bar-height bar-height 0
        float: right

    .bar-down
        background: rgba(#fff, .5)

    .bar-calc
        background: rgba(#ffff, .5)
        height: 2px
"""

render: -> """
    <div class="container">
        <table class="stats-container">
            <tr>
                <td class="stat"><span class="cup"></span></td>
                <td class="stat"><span class="limit"></span></td>
            </tr>
            <tr>
                <td class="label"><span class="label-cup">cup</span></td>
                <td class="label"><span class="label-limit">limit</span></td>
            </tr>
        </table>
        <div class="bar-container">
            <div class="bar bar-down"></div>
            <div class="bar bar-up"></div>
        </div>
        <div class="bar-container-2">
            <div class="bar bar-calc"></div>
            <div class="bar bar-cleft"></div>
        </div>
    </div>
"""

update: (output, domEl) ->

    updateStat = (prcnt, cup, limit, color) ->
        $(domEl).find(".bar-down").css "width", prcnt+"%"
        $(domEl).find(".bar-down").css background: color
        $(domEl).find(".label-cup").text cup+" GB ("+prcnt+"% of "+daysInMonthPrct()+")"
        $(domEl).find(".label-limit").text "Limit: "+limit+" GB"
        $(domEl).find(".bar-calc").css "width", daysInMonthPrct()
        $(domEl).find(".bar-calc").css background: color

    daysInMonthPrct = () ->
        today = new Date()
        month = today.getMonth() + 1
        year = today.getYear()+1900
        day = today.getDate()
        return Number(day * 100 / new Date(year, month, 0).getDate()).toFixed()+"%"


    args = output.split " "

    #808 of 1024 GB 78 #b846

    cup   = (Number) args[0]
    limit = (Number) args[2]
    unit  = (String) args[3]
    prcnt = (String) args[4]
    clr = (String) args[5]

    updateStat(prcnt, cup, limit, clr)

    #updateStat 'down', downBytes, totalBytes
    #updateStat 'up', upBytes, totalBytes
