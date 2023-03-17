import { Card, CardContent, Link, Typography } from '@mui/material';
import React from 'react'

function Show(title, rating, url, img) {
    return (
        /*<Card sx={{ minWidth: 275, padding: "1rem", marginLeft: "20rem", marginRight: "20rem"}} key={title}>
            <CardContent>
                <a href={url}><img src={img}/></a>
            </CardContent>
            <CardContent>
                <Typography sx={{ fontSize: 50, padding: "0.5rem", cursor: "grab"}} color="text.secondary" gutterBottom>
                    {title}
                </Typography>
                <Typography sx={{ fontSize: 42, padding: "0.5rem", cursor: "grab"}} color="text.secondary" gutterBottom>
                    {rating}
                </Typography>
            </CardContent>
        </Card>*/
        <div>
            <Card>

                <CardContent>
                    <Typography sx={{ fontSize: 50, cursor: "grab" }} color="text.secondary" gutterBottom>
                        <Link href={url}>{title}</Link>
                    </Typography>
                    <Typography sx={{ fontSize: 42, cursor: "grab" }} color="text.secondary" gutterBottom>
                        {rating}
                    </Typography>
                </CardContent>
                <CardContent>
                    <img src={img} />
                </CardContent>
            </Card>
        </div>
    )
}

export default Show;