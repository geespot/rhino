//
//  MasterViewController.h
//  RestfulIOSClient
//
//  Created by 孔 令开 on 13-5-14.
//  Copyright (c) 2013年 Egibbon. All rights reserved.
//

#import <UIKit/UIKit.h>

@class APIViewController;

@interface MasterViewController : UITableViewController

@property (strong, nonatomic) APIViewController* apiViewController;

@end
