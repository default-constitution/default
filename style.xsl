<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
        doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title><xsl:value-of select="/website/@title"/></title>
            <link rel="stylesheet" type="text/css" href="styles.css"/>
        </head>
        <body>
            <div id="content">
                <xsl:for-each select="/website/groupSections/groupSection">
                    <div class="group-title">
                        <xsl:value-of select="title"/>
                    </div>
                    <xsl:for-each select="contentSections/contentSection">
                        <div class="content-section">
                            <div class="content-title">
                                <a>
                                    <xsl:attribute name="href">
                                        <xsl:value-of select="url"/>
                                    </xsl:attribute>
                                    <xsl:value-of select="title"/>
                                </a>
                            </div>
                            <xsl:if test="image">
                                <img>
                                    <xsl:attribute name="src">
                                        <xsl:value-of select="image"/>
                                    </xsl:attribute>
                                </img>
                            </xsl:if>
                            <div class="content-description">
                                <xsl:value-of select="description"/>
                            </div>
                            <xsl:if test="hashtags">
                                <div class="content-hashtags">
                                    <xsl:value-of select="hashtags"/>
                                </div>
                            </xsl:if>
                        </div>
                    </xsl:for-each>
                    <div class="group-separator"></div>
                </xsl:for-each>
            </div>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
