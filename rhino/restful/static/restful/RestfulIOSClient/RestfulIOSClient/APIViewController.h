//
//  APIViewController.h
//  RestfulIOSClient
//
//  Created by 孔 令开 on 13-5-14.
//  Copyright (c) 2013年 Egibbon. All rights reserved.
//

#import <UIKit/UIKit.h>

@class DetailViewController;

@interface APIViewController : UITableViewController

@property (strong, nonatomic) DetailViewController* detailViewController;
@property (strong, nonatomic) NSArray* data;


@end
